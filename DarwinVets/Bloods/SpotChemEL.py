'''
Created on 30 Oct 2013

@author: richardm
'''
from SpotChemBase import SpotChemBase
from datetime import datetime

class SpotChemEL(SpotChemBase):
    '''
    classdocs
    '''

    def __init__(self, com_port):
        '''
        Constructor
        '''
        SpotChemBase.__init__(self, com_port, 9600, "scEL"+com_port[-1:])
        self._type = "electrolyte"
    
    def _handleBlock(self, block, endchar):
        self._result.addRawLine(block)

        dt  = block[0:14].strip()
        dt  = datetime.strptime(dt, "%y/%m/%d %H:%M")
        pid  = block[19:29].strip()
        stype = block[30:41].strip()
        
        self._result.setPatientID(pid)
        self._result.setDateTime(dt)
        self.info("blk: %s:%s:%s"%(pid, dt.ctime(), stype))

        pos = 42
        
        for i in range(3):
            result = block[pos:pos+21]
            pos = pos + 21

#             print "%d: %s"%(i, result)
            param =  result[0:5].strip()
            err   =  result[5:7].strip()
            try:
                val   =  float(result[7:12].strip())
            except ValueError:
                continue
            
            temp  =  result[12]
            units =  result[14:20].strip()
        
            self.info("     %s:%f %s"%(param, val, units))
            self._result.addParam(self._type, param, {
                    "val": val,
                    "units": units,
                    "err": err,
                    "temp": temp
                })
         
        return (True)   
