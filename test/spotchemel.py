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

    spotchem1 = SpotChemEL("TEST")
    
    spotchem1.registerResultHandler(rhandler)
    
    spotchem1.start()
    
    for dfname in datafiles:
        dfile = open(dfname, "rb")
        
        while True:
            d=dfile.read(16)
            if len(d) == 0:
                break
            spotchem1.testWrite(d)
            
        dfile.close()
    
    time.sleep(2)
    
    spotchem1.exit()
    
    spotchem1.join()