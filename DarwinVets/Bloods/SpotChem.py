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
    _RE_BLOCK    = re.compile('\002(.+)([\003\027])(.+)', re.DOTALL)
    _RE_DATETIME = re.compile('(\d{2})/(\d{2})/(\d{2}) +(\d{2}):(\d{2})')
    _RE_ID       = re.compile('ID# (\d+)')
    _RE_MULTI    = re.compile('MULTI:(.+)')
    _RE_SINGLE   = re.compile('SINGLE')
    _RE_PARAM    = re.compile('([A-Z]{1,5}) +([\036\037]{0,1})([1-9.]+) +([A-Z]+)([ +*])')

    def __init__(self, com_port, baudrate):
        '''
        Constructor
        '''
        BloodAnalyserBase.__init__(self, "spotchem")
        
        self._ser = serial.Serial(port=com_port, baudrate=baudrate, 
                                  bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                  stopbits=serial.STOPBITS_TWO,
                                  timeout=0.1)
        self._running = True
        self._state = "WAIT_BLOCK_START"
        self._data = ''

    def run(self):
        while self._running:
            rdata = self._ser.read(16)
            
            if not rdata:
                continue
            
            self._data = self._data + rdata
            match = SpotChem._RE_BLOCK.search(self._data)
            
            if match is None:
                continue
            
            block   = match.group(1)
            endchar = match.group(2)
            self._data = match.group(3)
            
            if self._result is None:
                self._result = Result()
            
            send = self._handleBlock(block, endchar)
            if send:
                self._sendResult()
                self._result = None
    
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
    
    def _sendResult(self):
        pass