from Result import Result
import couchdb


class BloodsDB():
    
    def __init__(self, dburl="http://127.0.0.1:5984/", dbname="vetbloods"):
        self._server = couchdb.Server(dburl)
        self._db = self._server[dbname]
        
        def save(docself):
            docself.objectify()
            self._db.save(docself._obj)
            
        setattr(Result, save.__name__, save)

    def getNoVetcom(self):
        return self._db.view("vetcom/novetcom", wrapper=lambda row:Result(row['value']))
        