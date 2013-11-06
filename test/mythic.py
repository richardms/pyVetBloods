import sys
import time
import logging
from DarwinVets.Bloods.Mythic import Mythic


datafiles = [ "data/mythic-2013-11-04T15:27.raw" ] #, "data/mythic-2013-11-02T18:01.raw" ]

def rhandler(res):
    print res
    cnlist = res.createCNs()
    for cn in cnlist:
        print "->%s<-"%cn

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    mythic = Mythic("TEST", 115200)
    
    mythic.registerResultHandler(rhandler)
    
    mythic.start()
    
    for dfname in datafiles:
        dfile = open(dfname, "rb")
        
        while True:
            d=dfile.read(16)
            if len(d) == 0:
                break
            mythic.testWrite(d)

        dfile.close()
    
    time.sleep(2)
    
    mythic.exit()
    
    mythic.join()
    