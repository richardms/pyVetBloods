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
        pid=res.id()
        if pid:
            an = vc.Animals(pid)
            if an is not None:
                res.addParam("vetcom", "an", an.dict())
                res.addParam("vetcom", "cl", an.Client().dict())
                res.save()
                
    for res in bdb.getNoNotes():
        notes = res.createCNs()
        res.addParam("notes", "list", notes)
        res.addParam("notes", "trfrd", 0)
        res.save()
        
        