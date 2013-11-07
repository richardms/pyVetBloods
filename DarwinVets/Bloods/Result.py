'''
Created on 24 Oct 2013

@author: richardm
'''

from datetime import datetime
import json
import dateutil.parser
import re

class Result(object):
    '''
    classdocs
    '''
    rtypes=['haem', 'electrolyte', 'biochem']
    rtinfo={
            'haem':        {'pretty':  "Haemotology", 'abrv': 'H', 'headliners': ['HCT', 'PLT', 'WBC']},
            'electrolyte': {'pretty':  "Electrolyte", 'abrv': 'E', 'headliners': ['BUN']},
            'biochem':     {'pretty': "Biochemistry", 'abrv': 'C', 'headliners': []}
            }
    _maxCNlen = 80
    _RE_ID = re.compile('^[0-9]+[0-9]{3}$')
    
    def __init__(self, srcobj=None):
        '''
        Constructor
        '''
        if srcobj is None:
            self._obj = {}
            self._datetime = datetime.now()
            self._datetime_recv = datetime.now()
        else:
            self._obj = srcobj
            self._datetime = dateutil.parser.parse(srcobj['datetime'])

    def id(self):
        if "id" in self._obj:
            pid = self._obj["id"]
            if Result._RE_ID.match(pid):
                return pid
        return 0 
        
    def getDatetime(self):
        return self._datetime
    
    def setTime(self, time):
        self._datetime = datetime.combine(self._datetime.date(), time)
        
    def setDate(self, date):
        self._datetime = datetime.combine(date, self._datetime.time())
        
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
        
    def getParam(self, location):
        loc = location.split('.')
        val = self._obj
        for l in loc:
            val = val[l]
        return val
    
    def createCNs(self, refRanges=None):
        cnlist = ["Internal Lab: %s"%(self._datetime.strftime("%H:%M %d/%m/%Y"))]
        rlist = []
        
        for rt in Result.rtypes:
            if rt not in self._obj:
                continue
            
            curline = ""
            
            resobj = dict(self._obj[rt])
            
            for r in Result.rtinfo[rt]['headliners']:
                res = resobj[r]
                if refRanges is not None:
                    mark = refRanges.getMark(self)
                else:
                    mark = "?"
                    
                rstr = "%s: %.2f %s, "%(r, res['val'], mark)
                
                curline = curline + rstr
                del resobj[r]
            
            if curline != "":
                rlist.append(curline[:-2])
                curline = ""
            
            for r in resobj:
                res = resobj[r]
                if refRanges is not None:
                    mark = refRanges.getMark(self)
                else:
                    mark = "?"
                    
                rstr = "%s: %.2f %s, "%(r, res['val'], mark)
                
                if len(curline) + len(rstr) > Result._maxCNlen-2:
                    rlist.append(curline[:-2])
                    curline = ""
                    
                curline = curline + rstr
                
            rlist.append(curline[:-2])
        
            for rstr in rlist:
                cnlist.append("%s %s"%(Result.rtinfo[rt]['abrv'], rstr))
        
        return cnlist

    def objectify(self):
        if datetime not in self._obj: 
            self._obj['datetime'] = self._datetime.isoformat()
        
       
    def __str__(self):
        rstr = "RESULT@"+self._datetime.isoformat()+"\n"
        rstr = rstr + json.dumps(self._obj)
        return rstr
    
