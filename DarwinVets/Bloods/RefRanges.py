'''
Created on 6 Nov 2013

@author: richardm
'''

import json

class RefRanges(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        
        dbfile = open(filename, "rb")
        self._db = json.load(dbfile)
        dbfile.close()
        
    def getMark(self, species, ttype, test, val):
        rng = self._db
        loc = [species.upper(), ttype.upper(), test.upper()]
        for l in loc:
            if l not in rng:
                return 'X'
            rng = rng[l]

        if val < rng['low']:
            return 'l'
        
        if val > rng['high']:
            return 'h'
        
        return ""