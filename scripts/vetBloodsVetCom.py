'''
Created on 6 Nov 2013

@author: richardm
'''
import logging
from DarwinVets.Bloods.BloodsDB import BloodsDB
from DarwinVets.Bloods.RefRanges import RefRanges

from PyVetCom import PyVetCom 
import time

def getVetcom(dbrefs):
    vc = dbrefs['vc']
    if vc is None:
        vc = PyVetCom()
    return vc

def doVetcom(dbrefs):
    bdb = dbrefs['bdb']
    for res in bdb.getNoVetcom():
        try:
            pid=res.id()
            if pid:
                vc = getVetcom(dbrefs)
                an = vc.Animals(pid)
                if an is not None:
                    res.addParam("vetcom", "an", an.dict())
                    res.addParam("vetcom", "cl", an.Client().dict())
                    res.save()
        except Exception, e:
            print "Exception in doVetcom: %s"%e
            

def doCreateNotes(dbrefs, refranges=None):
    bdb = dbrefs['bdb']
    for res in bdb.getNoNotes():
        notes = res.createCNs(refranges)
        res.addParam("notes", "list", notes)
        res.addParam("notes", "trfrd", 0)
        res.save()
        
def doWriteNotes(dbrefs):
    bdb = dbrefs['bdb']
    for res in bdb.getNotesNotTrfrd():
        try:
            anno = res.getParam('vetcom.an.ANNO')
        except KeyError:
            continue
        
        try:
            vc = getVetcom(dbrefs)
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
        except Exception, e:
            print "Exception in doWriteNotes: %s"%e

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bdb = BloodsDB("http://10.0.1.15:5984/")

    refranges = RefRanges('refranges.json')

    while True:
        dbrefs = {"bdb": bdb, "vc": None}
        doVetcom (dbrefs)
        doCreateNotes(dbrefs, refranges)
        doWriteNotes(dbrefs)
        if dbrefs['vc'] is not None:
            dbrefs['vc'].close()
        time.sleep(30)
        
