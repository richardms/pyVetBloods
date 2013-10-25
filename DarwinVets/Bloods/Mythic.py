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
    _RE_RES = re.compile('^MYTHIC.+RESULT[ ]{0,1};')
    _RE_RES_END = re.compile('^END_RESULT[ ]{0,1}')

    def __init__(self, com_port, baudrate):
        '''
        Constructor
        '''
        BloodAnalyserBase.__init__(self, "mythic")

        self._ser = serial.Serial(port=com_port, baudrate=baudrate, 
                                  bytesize=serial.EIGHTBITS, timeout=0.1)
        self._state = "WAIT_REQ"
        self._handler = None
        
        self._inbuf = ""
        
    def run(self):
        while self._running:
            line = self._readline()
            
            if line == "":
                continue
            
            if self._state == "WAIT_REQ":
                self._handle_WAIT_REQ(line)
            elif self._state == "WAIT_RESULT":
                self._handle_WAIT_RESULT(line)
            elif self._state == "RECV_RESULT":
                self._handle_RECV_RESULT(line)
    
    def _readline(self):
        data = self._inbuf + self._ser.read(16)
        
        for i in range(len(data)):
            if data[i] == '\r':
                line=data[0:i].strip()
                self._inbuf=data[i+1:]
                return line
            
        return ""
    
    def _handle_WAIT_REQ(self, line):
        if Mythic._RE_REQ.match(line) is None:
            return
        self._ser.write(Mythic._ACK_RES_READY)
        self._state = "WAIT_RESULT"
        
        return
    
    def _handle_WAIT_RESULT(self, line):
        if Mythic._RE_RES.match(line) is None:
            return
        
        self._cur_result = Result()
        self._state = "RECV_RESULT"
        
        return

    def _handle_RECV_RESULT(self, line):
        if Mythic._RE_REQ_END.match(line) is None:
            self._ser.write(Mythic._ACK_RESULT)
            self._state = "WAIT_REQ"
            
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
        
    def _parse_DATE(self, parts):
        dt = datetime.strptime(parts[1], "%s/%m/%y")
        self._cur_result.setDate(dt.date())
        
    def _parse_TIME(self, parts):
        dt = datetime.strptime(parts[1], "%H:%M:%S")
        self._cur_result.setTime(dt.time())
    
    def _parse_StdParam(self, parts):
        pass
    
    def _parse_MythicParam(self, parts):
        pass
    
    def _parse_MythicId(self, parts):
        pass
        
    _LINE_PARSERS={
                "DATE": (_parse_DATE),
                "TIME": (_parse_TIME),
                "MODE": (_parse_MythicParam),
                "UNIT": (_parse_MythicParam),
                "SEQ":  (_parse_MythicParam),
                "SID":  (_parse_MythicParam),
                "PID":  (_parse_MythicParam),
                "ID":   (_parse_MythicId),
                "TYPE": (_parse_MythicParam),
                "TEST": (_parse_MythicParam),
                "OPERATOR":   (_parse_MythicParam),
                "PREL":       (_parse_MythicParam),
                "CYCLE":      (_parse_MythicParam),
                "WBC":  (_parse_StdParam),
                "RBC":  (_parse_StdParam),
                "HGB":  (_parse_StdParam),
                "HCT":  (_parse_StdParam),
                "MCV":  (_parse_StdParam),
                "MCH":  (_parse_StdParam),
                "MCHC": (_parse_StdParam),
                "RDW":  (_parse_StdParam),
                "PLT":  (_parse_StdParam),
                "MPV":  (_parse_StdParam),
                "PCT":  (_parse_StdParam),
                "PDW":  (_parse_StdParam),
                "LYM%": (_parse_StdParam),
                "MON%": (_parse_StdParam),
                "NEU%": (_parse_StdParam),
                "EOS%": (_parse_StdParam),
                "BAS%": (_parse_StdParam),
                "LYM":  (_parse_StdParam),
                "MON":  (_parse_StdParam),
                "NEU":  (_parse_StdParam),
                "EOS":  (_parse_StdParam),
                "BAS":  (_parse_StdParam),                
                }
        