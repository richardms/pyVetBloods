'''
Created on 25 Oct 2013

@author: richardm
'''

from BloodAnalyserBase import BloodAnalyserBase
import serial
import re
import Result

class SpotChemBase(BloodAnalyserBase):
    '''
    classdocs
    '''
    _RE_BLOCK    = re.compile('\002(.+)([\003\027])(.*)', re.DOTALL)

    def __init__(self, com_port, baudrate, bid):
        '''
        Constructor
        '''
        BloodAnalyserBase.__init__(self, bid)
        
        if com_port=="TEST":
            self._ser = self._testmode()
        else:
            self._ser = serial.Serial(port=com_port, baudrate=baudrate, 
                                  bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                  stopbits=serial.STOPBITS_TWO,
                                  timeout=0.1)
        self._running = True
        self._state = "WAIT_BLOCK_START"
        self._data = ''
        self._result = None

    def run(self):
        self.debug("Running")
        while self._running:
            rdata = self._read(16)
            
            if rdata == "":
                continue

            self._data = self._data + rdata
            match = SpotChemBase._RE_BLOCK.search(self._data)
            
            if match is None:
                continue
            
            block   = match.group(1)
            endchar = match.group(2)
            self._data = match.group(3)
            
#             self.debug("Block '%s'", block)
            
            if self._result is None:
                self.debug("Creating new Result")
                self._result = Result.Result()
            
            send = self._handleBlock(block, endchar)
            if send:
                self._sendResult()
                self._result = None
        
        if self._raw is not None:
            self._raw.close()
        self._ser.close()
        self.debug("Run finished")

    
