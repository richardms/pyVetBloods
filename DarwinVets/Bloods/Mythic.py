'''
Created on 24 Oct 2013

@author: richardm
'''

from BloodAnalyserBase import BloodAnalyserBase
import serial
import re
import Result
from datetime import datetime

class Mythic(BloodAnalyserBase):
    '''
    classdocs
    '''
    _ACK_RES_READY='ACK_RESULT_READY\r'
    _ACK_RESULT='ACK_RESULT;OK; \r'

    _RE_REQ = re.compile('^MYTHIC.+RESULT_READY')
    _RE_RES = re.compile('^MYTHIC.+RESULT[ ]{0,1}$')
    _RE_RES_END = re.compile('^END_RESULT[ ]{0,1}')

    _RE_PID = re.compile('^[1-9][0-9]{3,}$')

    def __init__(self, com_port, baudrate):
        '''
        Constructor
        '''
        BloodAnalyserBase.__init__(self, "mythic")

        self._type = "haem"

        if com_port=="TEST":
            self._ser = self._testmode()
        else:
            self._ser = serial.Serial(port=com_port, baudrate=baudrate, 
                                  bytesize=serial.EIGHTBITS, timeout=0.1)
        self._state = "WAIT_REQ"
        
        self._inbuf = ""
        
    def run(self):
        self.debug("Running")

        while self._running:
            line = self._readline()
            if line == "":
                continue
            
            self.debug("Got '%s' in state %s", line, self._state)

            if self._state == "WAIT_REQ":
                self._handle_WAIT_REQ(line)
            elif self._state == "WAIT_RESULT":
                self._handle_WAIT_RESULT(line)
            elif self._state == "RECV_RESULT":
                self._handle_RECV_RESULT(line)

        if self._raw is not None:
            self._raw.close()
        self._ser.close()
        self.debug("Run finished")

    
    def _readline(self):
        self._inbuf = self._inbuf + self._read(16)

        for i in range(len(self._inbuf)):
            if self._inbuf[i] == '\r':
                line=self._inbuf[0:i].strip()
                self._inbuf=self._inbuf[i+1:]
                return line
            
        return ""
    
    def _handle_WAIT_REQ(self, line):
        if Mythic._RE_REQ.match(line) is None:
            return
        self._write(Mythic._ACK_RES_READY)
        self._state = "WAIT_RESULT"
        
        return
    
    def _handle_WAIT_RESULT(self, line):
        if Mythic._RE_RES.match(line) is None:
            self._state = "WAIT_REQ"
            return
        
        self._result = Result.Result()
        self._state = "RECV_RESULT"
        
        return

    def _handle_RECV_RESULT(self, line):
        if Mythic._RE_RES_END.match(line) is not None:
            self._write(Mythic._ACK_RESULT)
            self._state = "WAIT_REQ"
            self._sendResult()
            return
        
        self._parseResult(line)
        
        return
    
    def _parseResult(self, line):
        splitline=[ s.strip() for s in line.split(';') ]
        try:
            parser=Mythic._LINE_PARSERS[splitline[0]]
        except KeyError :
            return
        
        return parser[0](self, splitline, parser[1:])
        
    def _parse_DATE(self, parts, extlist):
        dt = datetime.strptime(parts[1], "%d/%m/%Y")
        self._result.setDate(dt.date())
        
    def _parse_TIME(self, parts, extlist):
        dt = datetime.strptime(parts[1], "%H:%M:%S")
        self._result.setTime(dt.time())
    
    def _parse_StdParam(self, parts, extlist):
        valstr = parts[1]
#         self.info("StdParam %s: %s"%(parts[0], parts[1]))
        try:
            val = float(valstr)
            if parts[2] != "":
                mark = "REJECTED"
            else:
                mark = parts[3]
                
            self._result.addParam(self._type, parts[0], {
                    "val": val,
                    "mark": mark
            })
        except ValueError:
            self.warn("No value for %s"%valstr)
            if (valstr == "....."):
                mark = "INVALID"
            else:
                mark = "TOO HIGH"
            self._result.addParam(self._type, parts[0], {
                    "mark": mark
            })

    
    def _parse_MythicParam(self, parts, extlist):
        self.info("MythicParam %s: %s"%(parts[0], parts[1]))
        self._result.addParam("mythic", parts[0], parts[1])
    
    def _parse_MythicId(self, parts, extlist):
        self.info("Try ID %s"%(parts[1]))
        if Mythic._RE_PID.match(parts[1]):
            self.info("Set patient ID %s"%(parts[1]))
            self._result.setPatientID(parts[1])
        else:
            self._result.addParam("mythic", "id", parts[1])
    
        
    _LINE_PARSERS={
                "DATE": (_parse_DATE, ),
                "TIME": (_parse_TIME, ),
                "MODE": (_parse_MythicParam, ),
                "UNIT": (_parse_MythicParam, ),
                "SEQ":  (_parse_MythicParam, ),
                "SID":  (_parse_MythicParam, ),
                "PID":  (_parse_MythicId, ),
                "ID":   (_parse_MythicId, ),
                "TYPE": (_parse_MythicParam, ),
                "TEST": (_parse_MythicParam, ),
                "OPERATOR":   (_parse_MythicParam, ),
                "PREL":       (_parse_MythicParam, ),
                "CYCLE":      (_parse_MythicParam, ),
                "WBC":  (_parse_StdParam, ),
                "RBC":  (_parse_StdParam, ),
                "HGB":  (_parse_StdParam, ),
                "HCT":  (_parse_StdParam, ),
                "MCV":  (_parse_StdParam, ),
                "MCH":  (_parse_StdParam, ),
                "MCHC": (_parse_StdParam, ),
                "RDW":  (_parse_StdParam, ),
                "PLT":  (_parse_StdParam, ),
                "MPV":  (_parse_StdParam, ),
                "PCT":  (_parse_StdParam, ),
                "PDW":  (_parse_StdParam, ),
                "LYM%": (_parse_StdParam, ),
                "MON%": (_parse_StdParam, ),
                "NEU%": (_parse_StdParam, ),
                "EOS%": (_parse_StdParam, ),
                "BAS%": (_parse_StdParam, ),
                "LYM":  (_parse_StdParam, ),
                "MON":  (_parse_StdParam, ),
                "NEU":  (_parse_StdParam, ),
                "EOS":  (_parse_StdParam, ),
                "BAS":  (_parse_StdParam, ),
                }
        