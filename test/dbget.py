'''
Created on 6 Nov 2013

@author: richardm
'''
import logging
from DarwinVets.Bloods.BloodsDB import BloodsDB
from PyVetCom import PyVetCom 

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bdb = BloodsDB("http://10.0.1.15:5984/")
    
    vc = PyVetCom()

    for res in bdb.getNoVetcom():
        print res
        if res.id:
            an = vc.Animals(res.id)
    