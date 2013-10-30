import serial
import sys
import time
from DarwinVets.Bloods.SpotChemEZ import SpotChemEZ
import logging


datafiles = [ "test/data/spotchem1-2013-10-30T12:08.raw", "test/data/spotchem1-2013-10-30T13:15.raw" ]

def rhandler(res):
    print res

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    spotchem1 = SpotChemEZ("TEST", 9600)
    
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