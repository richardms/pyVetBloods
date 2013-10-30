'''
Created on 24 Oct 2013

@author: richardm
'''

from datetime import datetime
import json

class Result(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._datetime = datetime.now()
        self._datetime_recv = datetime.now()
        self._obj = {}
        
    def setTime(self, time):
        self._datetime = datetime(self._datetime.date(), time)
        
    def setDate(self, date):
        self._datetime = datetime(date, self._datetime.time())
        
    def setDateTime(self, dt):
        self._datetime = dt
        
    def setPatientID(self, pid):
        self._obj["id"] = pid
        
    def addParam(self, part, key, value):
        try:
            p = self._obj[part]
        except KeyError:
            p = {}
            self._obj[part] = p
            
        p[key]=value
        
    def __str__(self):
        rstr = "RESULT@"+self._datetime.isoformat()+"\n"
        rstr = rstr + json.dumps(self._obj)
        return rstr
    