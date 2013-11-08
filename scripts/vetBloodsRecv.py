'''
Created on 8 Nov 2013

@author: richardm
'''
from DarwinVets.Bloods.SpotChemEZ import SpotChemEZ
from DarwinVets.Bloods.SpotChemEL import SpotChemEL
from DarwinVets.Bloods.Mythic import Mythic
from DarwinVets.Bloods.BloodsDB import BloodsDB

import sys
import logging
import time
from datetime import datetime

def rhandler(res):
    print res
    res.save()

if __name__ == '__main__':
    logging.basicConfig(filename=datetime.now().isoformat()[0:16]+'.log',level=logging.DEBUG)

    bdb = BloodsDB()

    mythic = Mythic("/dev/ttyUSB0", 115200)
    spotchemez = SpotChemEZ("/dev/ttyUSB1", 9600)
    spotchemel = SpotChemEL("/dev/ttyUSB2")
    
    mythic.registerResultHandler(rhandler)
    spotchemez.registerResultHandler(rhandler)
    spotchemel.registerResultHandler(rhandler)
    
    mythic.saveRaw()
    spotchemez.saveRaw()
    spotchemel.saveRaw()
    
    mythic.start()
    spotchemez.start()
    spotchemel.start()

#     def sigint_handler(sig, frame):
#         print 'You pressed Ctrl+C - exiting'
#         mythic.exit()
#         spotchem.exit()
#     
#     signal.signal(signal.SIGINT, sigint_handler)
    
    try:
        while True:
            raw_input("Press Ctrl-C to exit\n")
    except:
        mythic.exit()
        spotchemez.exit()
        spotchemel.exit()

    mythic.join()
    spotchemez.join()
    spotchemel.join()
    
    sys.exit(0)
    
