'''
Created on 25 Oct 2013

@author: richardm
'''
import threading
import logging
import tempfile
import os
from datetime import datetime

class BloodAnalyserError(Exception):
    def __init__(self, msg):
        self.msg = msg

class BloodAnalyserBase(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, bid):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.daemon = True
        
        self._running = True
        self._result = None
        
        self._id=bid
        self._logger = logging.getLogger("%6s"%self._id)

        self._handler = None
        self._raw = None
        
        self._test = False
        
        self.debug("Constructed")

    def exit(self):
        self.debug("Told to exit")
        self.testClose()
        self._running = False
        
    def registerResultHandler(self, handler):
        self._handler = handler
        
    def _sendResult(self):
        if self._handler is None or self._result is None:
            return
        self._handler(self._result)
        
    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
        raise BloodAnalyserError(msg)
    
    def warn(self, msg, *args, **kwargs): 
        self._logger.warn(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs): 
        self._logger.info(msg, *args, **kwargs)
        
    def debug(self, msg, *args, **kwargs): 
        self._logger.debug(msg, *args, **kwargs)
        
    def saveRaw(self, fname=None):
        if fname is None:
            fname=self._id+"-"+datetime.now().isoformat()[0:16]+".raw"
        
        self._raw = open(fname, "wb")

        
    def _read(self, rlen=16):
        rdata = self._ser.read(rlen)
        
        if self._raw is not None:
            self._raw.write(rdata)
            self._raw.flush()
        
        return rdata

    def _write(self, d):
        if self._test:
            self.info("Write: %s"%d)
        else:
            self._ser.write(d)

    def _testmode(self):
        self._test = True
#         self._test_fifoname = tempfile.mktemp(prefix=self._id+"-", suffix='.pipe')
#         self.debug("Test mode. FIFO=%s"%self._test_fifoname)
#         os.mkfifo(self._test_fifoname)
#         
#         ser = open(self._test_fifoname, "rb", 0)
#         self._test_wfile = open(self._test_fifoname, "wb", 0)
        p = os.pipe()
        self._test_wfile = os.fdopen(p[1], 'w')
        return os.fdopen(p[0])
    
    def testWrite(self, d):
        if self._test:
            self._test_wfile.write(d)
            self._test_wfile.flush()
            
    def testClose(self):
        if self._test:
            self._test_wfile.close()
