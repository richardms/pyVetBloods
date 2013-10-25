'''
Created on 25 Oct 2013

@author: richardm
'''

from DarwinVets.Bloods.SpotChem import SpotChem
from DarwinVets.Bloods.Mythic import Mythic

if __name__ == '__main__':
    mythic = Mythic("/dev/ttyUSB0", 9600)
    spotchem = SpotChem("/dev/ttyUSB1", 9600)
    
    mythic.start()
    spotchem.start()
    