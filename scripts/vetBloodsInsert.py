'''
Created on 8 Nov 2013

@author: richardm
'''
import serial
import sys
import time
from DarwinVets.Bloods.SpotChemEL import SpotChemEL
from DarwinVets.Bloods.SpotChemEZ import SpotChemEZ
from DarwinVets.Bloods.Mythic import Mythic
import logging
from DarwinVets.Bloods.BloodsDB import BloodsDB
import re

def rhandler(res):
    print res
    res.save()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bdb = BloodsDB()

    fname = sys.argv[1]
    
    if re.match('mythic-', fname):
        print "Mythic"
        analyser = Mythic("TEST", 115200)
    elif re.match('scEZ', fname):
        analyser = SpotChemEZ("TEST", 9600)
    elif re.match('scEL', fname):
        analyser = SpotChemEL("TEST")
    else:
        print "Unknown analyser for '%s'"%fname
        sys.exit(1)
    
    analyser.registerResultHandler(rhandler)
    
    analyser.start()

    print "Reading %s"%fname    
    dfile = open(fname, "rb")
        
    while True:
        d=dfile.read(16)
        if len(d) == 0:
            break
        analyser.testWrite(d)
            
    dfile.close()
    
    time.sleep(2)
    
    analyser.exit()
    
    analyser.join()
    
