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

    mythic = Mythic("/dev/ttyUSB0", 9600)
    spotchem = SpotChem("/dev/ttyUSB1", 9600)
    
    mythic.start()
    spotchem.start()

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
        mythic.exit()
        spotchem.exit()

    mythic.join()
    spotchem.join()
    
    sys.exit(0)
    