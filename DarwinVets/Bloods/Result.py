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
    rtypes=['haem', 'electrolyte', 'biochem']
    rtinfo={'haem': {'pretty': "Haemotology", 'abrv': 'H'},
            'electrolyte': {'pretty': "Electrolyte", 'abrv': 'E'},
            'biochem': {'pretty': "Biochemistry", 'abrv': 'C'}
            }

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
        
    def createCNs(self, refRanges=None):
        cnlist = ["Internal Lab: %s"%(self.id, self.datetime.strftime("%H:%M %d/%m/%Y"))]
        rlist = []
        
        for rt in Result.rtypes:
            if rt not in self._obj:
                continue
            
            curline = ""
            
            for r in self._obj[rt]:
                res = self._obj[rt][r]
                if refRanges is not None:
                    mark = refRanges.getMark(self)
                else:
                    mark = "?"
                    
                rstr = "%s: %.2f %s, "%(r, res.val, mark)
                
                if len(curline) + len(rstr) > Result._maxCNlen:
                    rlist.append(curline[:-2])
                    curline = ""
                    
                curline = curline + rstr
        rlist.append(curline[:-2])
        
        for rstr in rlist:
            cnlist.append("%s %s"%(Result.rtinfo[rt].abrv, rstr))
        
        return cnlist

        
    def __str__(self):
        rstr = "RESULT@"+self._datetime.isoformat()+"\n"
        rstr = rstr + json.dumps(self._obj)
        return rstr
    