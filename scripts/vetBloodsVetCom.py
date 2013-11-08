'''
Created on 6 Nov 2013

@author: richardm
'''
import logging
from DarwinVets.Bloods.BloodsDB import BloodsDB
from PyVetCom import PyVetCom 
import time

def doVetcom(bdb, vc):
    for res in bdb.getNoVetcom():
        pid=res.id()
        if pid:
            an = vc.Animals(pid)
            if an is not None:
                res.addParam("vetcom", "an", an.dict())
                res.addParam("vetcom", "cl", an.Client().dict())
                res.save()

def doCreateNotes(bdb, vc):
    for res in bdb.getNoNotes():
        notes = res.createCNs()
        res.addParam("notes", "list", notes)
        res.addParam("notes", "trfrd", 0)
        res.save()
        
def doWriteNotes(bdb, vc):
    for res in bdb.getNotesNotTrfrd():
        try:
            anno = res.getParam('vetcom.an.ANNO')
        except KeyError:
            continue
        
        date = vc.convDate(res.getDatetime())
        lineno = vc.Notes().                          \
            eq('ANNO', anno).                         \
            eq('DATETIME', date).                     \
            max('LINENO') + 1
        
        notes = res.getParam('notes.list')
        for n in notes:
            vcnote = {
                      'TYPE': 'L',
                      'ANNO': anno, 
                      'DATETIME': date, 
                      'TEXT': n.encode('utf-8'), 
                      'INITS': 'INT', 
                      'LINENO': lineno
                      }
            print vcnote
            vc.Notes.insert(vcnote)
            lineno = lineno+1
        vc.Notes.commit()
        res.addParam("notes", "trfrd", 1)
        res.save()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bdb = BloodsDB("http://192.168.3.117:5984/")
    
    vc = PyVetCom()

    while True:
        doVetcom (bdb, vc)
        doCreateNotes(bdb, vc)
        doWriteNotes(bdb, vc)
        time.sleep(30)
        
