import serial
import sys
import time
from DarwinVets.Bloods.SpotChemEL import SpotChemEL
import logging


datafiles = [ "data/scEL2-2013-10-30T18:12.raw" ]

def rhandler(res):
    print res

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    spotchemel = SpotChemEL("TEST")
    
    spotchemel.registerResultHandler(rhandler)
    
    spotchemel.start()
    
    for dfname in datafiles:
        dfile = open(dfname, "rb")
        
        while True:
            d=dfile.read(16)
            if len(d) == 0:
                break
            spotchemel.testWrite(d)
            
        dfile.close()
    
    time.sleep(2)
    
    spotchemel.exit()
    
    spotchemel.join()
    