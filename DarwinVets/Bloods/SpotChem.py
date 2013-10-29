'''
Created on 25 Oct 2013

@author: richardm
'''

from BloodAnalyserBase import BloodAnalyserBase
import serial
import re
import Result
from datetime import datetime

class SpotChem(BloodAnalyserBase):
    '''
    classdocs
    '''
    _RE_BLOCK    = re.compile('\002(.+)([\003\027])(.*)', re.DOTALL)
    _RE_DATETIME = re.compile('(\d{2})/(\d{2})/(\d{2}) +(\d{2}):(\d{2})')
    _RE_ID       = re.compile('ID# (\d+)')
    _RE_MULTI    = re.compile('MULTI:(.+)')
    _RE_SINGLE   = re.compile('SINGLE')
    _RE_PARAM    = re.compile('([A-Z]{1,5}) +([\036\037]{0,1})([1-9.]+) +([A-Z]+)([ +*])')

    def __init__(self, com_port, baudrate):
        '''
        Constructor
        '''
        BloodAnalyserBase.__init__(self, "spotchem"+com_port[-1:])
        
        self._ser = serial.Serial(port=com_port, baudrate=baudrate, 
                                  bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                  stopbits=serial.STOPBITS_TWO,
                                  timeout=0.1)
        self._running = True
        self._state = "WAIT_BLOCK_START"
        self._data = ''
        self._result = None
        self._raw = None

    def run(self):
        self.debug("Running")
        while self._running:
            rdata = self._read(16)
            
            if rdata == "":
                continue

            self._data = self._data + rdata
            match = SpotChem._RE_BLOCK.search(self._data)
            
            if match is None:
                continue
            
            block   = match.group(1)
            endchar = match.group(2)
            self._data = match.group(3)
            
            self.debug("Block '%s'", block)
            
            if self._result is None:
                self.debug("Creating new Result")
                self._result = Result.Result()
            
            send = self._handleBlock_fmt2(block, endchar)
            if send:
                self._sendResult()
                self._result = None
        
        if self._raw is not None:
            self._raw.close()
        
        self.debug("Run finished")

    def saveRaw(self, fname):
        if fname is None:
            fname=self._id+"-"+datetime.now().isoformat()[0:16]+".raw"
        
        self._raw = open(fname, "wb")

    def _read(self, rlen=16):
        rdata = self._ser.read(rlen)
        
        if self._raw is not None:
            self._raw.write(rdata)
        
        return rdata
    
    def _handleBlock(self, block, endchar):
        parts=[ s.strip() for s in block.split('\n')]
        
        # Test for date line
        m = SpotChem._RE_DATETIME.match(parts[0])
        if m:
            dt = datetime(m.group(1),
                          m.group(2),
                          m.group(3),
                          m.group(4),
                          m.group(5),
                          m.group(6))
            self._result.setDatetime(dt)
            m = self._RE_ID.match(parts[1])
            if m:
                self._result.setId(m.group(1))
            parts=parts[2:]
            
        for p in parts:
            m = SpotChem._RE_PARAM.match(p)
            if m:
                name  = m.group(1)
                val   = m.group(3)
                units = m.group(4)
                level_ind = m.group(2)
                temp = m.group(5)
                
                self._result.addParam(self._type, name, {
                        val: val,
                        units: units,
                        level_ind: level_ind,
                        temp: temp
                    })
         
        return (endchar == "\003")   
    
    def _handleBlock_fmt2(self, block, endchar):
        pid  = block[:10].strip()
        maxc = int(block[13:15].strip())
        cnt = int(block[16:18].strip())
        dt  = block[19:33].strip()
        dt  = datetime.strptime(dt, "%y/%m/%d %H:%M")
        err = block[34]
        temp = block[36]
        multi = block[39:49].strip()
        param = block[50:55].strip()
        val   = float(block[56:61].strip())
        units = block[62:68].strip()
        
        print "blk: %s:%d/%d:%s:%s:%s"%(pid, maxc, cnt, dt.ctime(), err, temp)
        print "     %s:%s:%f %s"%(multi, param, val, units)
#                 self._result.addParam(self._type, name, {
#                         val: val,
#                         units: units,
#                         level_ind: level_ind,
#                         temp: temp
#                     })
         
        return (endchar == "\003")   
    
    def _sendResult(self):
        pass
    
    
if __name__ == '__main__':
   sc = SpotChem("/dev/ttyUSB0", 9600)
   sc._handleBlock_fmt2("26872      11 6/ 1 13/10/29 10:37 0 0\n\rPANEL-V    BUN    11.7 mmol/L 0         \n\r","\003")
