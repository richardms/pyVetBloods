'''
Created on 25 Oct 2013

@author: richardm
'''

from DarwinVets.Bloods.SpotChem import SpotChem
from DarwinVets.Bloods.Mythic import Mythic
import signal
import sys
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

#    mythic = Mythic("/dev/ttyUSB0", 9600)
    spotchem = SpotChem("/dev/ttyUSB0", 9600)
    spotchem1 = SpotChem("/dev/ttyUSB1", 9600)
    spotchem2 = SpotChem("/dev/ttyUSB2", 9600)
    
    spotchem.saveRaw()
    spotchem1.saveRaw()
    spotchem2.saveRaw()
    
    spotchem.start()
    spotchem1.start()
    spotchem2.start()

#     def sigint_handler(sig, frame):
#         print 'You pressed Ctrl+C - exiting'
#         mythic.exit()
#         spotchem.exit()
#     
#     signal.signal(signal.SIGINT, sigint_handler)
    
    try:
        while True:
            raw_input("Press Ctrl-C to exit")
    except:
        spotchem.exit()
        spotchem1.exit()
        spotchem2.exit()

    spotchem.join()
    spotchem1.join()
    spotchem2.join()
    
    sys.exit(0)
    
