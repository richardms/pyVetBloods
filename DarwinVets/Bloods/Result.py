'''
Created on 24 Oct 2013

@author: richardm
'''

from datetime import datetime


class Result(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._datetime = datetime.now()
        self._obj = {}
        
    def setTime(self, time):
        self._datetime = datetime(self._datetime.date(), time)
        
    def setDate(self, date):
        self._datetime = datetime(date, self._datetime.time())
        
    def setParam(self, part, key, value):
        try:
            p = self._obj[part]
        except KeyError:
            p = {}
            self._obj[part] = p
            
        p[key]=value