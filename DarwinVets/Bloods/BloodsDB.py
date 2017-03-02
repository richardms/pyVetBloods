from Result import Result
import couchdb

class BloodsDB():
    
    def __init__(self, dburl="http://127.0.0.1:5984/", dbname="vetbloods_raw"):
        self._server = couchdb.Server(dburl)
        self._db = self._server[dbname]
        
        def save(docself):
            docself.objectify()
            print docself._obj
            self._db.save(docself._obj)
            
        setattr(Result, save.__name__, save)

    def getNoVetcom(self):
        return self._db.view("vetcom/none", wrapper=lambda row:Result(row['value']))

    def getNoNotes(self):
        return self._db.view("notes/none", wrapper=lambda row:Result(row['value']))
    
    def getNotesNotTrfrd(self):
        return self._db.view("notes/not_trfrd", wrapper=lambda row:Result(row['value']))

