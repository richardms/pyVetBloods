'''
Created on 30 Oct 2013

@author: richardm
'''

from SpotChemBase import SpotChemBase
import re
from datetime import datetime

class SpotChemEZ(SpotChemBase):
    '''
    classdocs
    '''
    _RE_DATETIME = re.compile('(\d{2})/(\d{2})/(\d{2}) +(\d{2}):(\d{2})')
    _RE_ID       = re.compile('ID# (\d+)')
    _RE_MULTI    = re.compile('MULTI:(.+)')
    _RE_SINGLE   = re.compile('SINGLE')
    _RE_PARAM    = re.compile('([A-Z]{1,5}) +([\036\037]{0,1})([1-9.]+) +([A-Z]+)([ +*])')

    def __init__(self, com_port, baudrate):
        '''
        Constructor
        '''
        SpotChemBase.__init__(self, com_port, baudrate, "scEZ"+com_port[-1:])
        self._type = "biochem"
        
        SpotChemEZ._handleBlock = SpotChemEZ._handleBlock_fmt2

    
    # UNTESTED!!!
    def _handleBlock_fmt1(self, block, endchar):
        self._result.addRawLine(block)

        parts=[ s.strip() for s in block.split('\n')]
        
        # Test for date line
        m = SpotChemEZ._RE_DATETIME.match(parts[0])
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
            m = SpotChemEZ._RE_PARAM.match(p)
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
        self._result.addRawLine(block)

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
        
        if cnt == 1:
            self._result.setPatientID(pid)
            self._result.setDateTime(dt)

        self.info("blk: %s:%d/%d:%s:%s:%s"%(pid, maxc, cnt, dt.ctime(), err, temp))
        self.info("     %s:%s:%f %s"%(multi, param, val, units))
        self._result.addParam(self._type, param, {
                    "val": val,
                    "units": units,
                    "err": err,
                    "temp": temp
            })
#                 self._result.addParam(self._type, name, {
#                         val: val,
#                         units: units,
#                         level_ind: level_ind,
#                         temp: temp
#                     })
         
        return (cnt == maxc)   
    
if __name__ == '__main__':
    sc = SpotChemEZ("/dev/ttyUSB0", 9600)
    sc._handleBlock_fmt2("26872      11 6/ 1 13/10/29 10:37 0 0\n\rPANEL-V    BUN    11.7 mmol/L 0         \n\r","\003")
