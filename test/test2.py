'''
Created on 25 Oct 2013

@author: richardm
'''

from DarwinVets.Bloods.SpotChemEZ import SpotChemEZ
from DarwinVets.Bloods.SpotChemEL import SpotChemEL
from DarwinVets.Bloods.Mythic import Mythic
import sys
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    mythic = Mythic("/dev/ttyUSB0", 115200)
    spotchem1 = SpotChemEZ("/dev/ttyUSB1", 9600)
    spotchem2 = SpotChemEL("/dev/ttyUSB2")
    
    mythic.saveRaw()
    spotchem1.saveRaw()
    spotchem2.saveRaw()
    
    mythic.start()
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
            raw_input("Press Ctrl-C to exit\n")
    except:
        mythic.exit()
        spotchem1.exit()
        spotchem2.exit()

    mythic.join()
    spotchem1.join()
    spotchem2.join()
    
    sys.exit(0)
    
