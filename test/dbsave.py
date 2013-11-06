import serial
import sys
import time
from DarwinVets.Bloods.SpotChemEZ import SpotChemEZ
import logging
from DarwinVets.Bloods.BloodsDB import BloodsDB


datafiles = [ "data/spotchem1-2013-10-30T12:08.raw", "data/spotchem1-2013-10-30T13:15.raw" ]

def rhandler(res):
    print res
    res.save()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bdb = BloodsDB()

    spotchemez = SpotChemEZ("TEST", 9600)
    
    spotchemez.registerResultHandler(rhandler)
    
    spotchemez.start()
    
    for dfname in datafiles:
        dfile = open(dfname, "rb")
        
        while True:
            d=dfile.read(16)
            if len(d) == 0:
                break
            spotchemez.testWrite(d)
            
        dfile.close()
    
    time.sleep(2)
    
    spotchemez.exit()
    
    spotchemez.join()
    