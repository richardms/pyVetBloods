'''
Created on 25 Oct 2013

@author: richardm
'''
import threading
import logging

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
        self._cur_result = None
        
        self._id=bid
        self._logger = logging.getLogger("%10s"%self._id)
        
        self.debug("Constructed")

    def exit(self):
        self.debug("Told to exit")
        self._running = False
        
    def registerResultHandler(self, handler):
        self._handler = handler
        
    def _sendResult(self):
        if self._handler is None:
            return
        self._handler(self._cur_result)
        
    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
        raise BloodAnalyserError(msg)
    
    def warn(self, msg, *args, **kwargs): 
        self._logger.warn(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs): 
        self._logger.warn(msg, *args, **kwargs)
        
    def debug(self, msg, *args, **kwargs): 
        self._logger.debug(msg, *args, **kwargs)
        
    