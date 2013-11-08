import couchdb

dburl="http://127.0.0.1:5984/"
dbname="vetbloods"

server = couchdb.Server(dburl)

server.delete(dbname)

try:
    db = server[dbname]
except:
    db = server.create(dbname)        

views_vetcom = {
  "_id": "_design/vetcom",
  "views": {
    "none": {
      "map": '''function(doc) {
        if (!doc.vetcom) {
          emit(doc._id, doc) ;
        } 
      }'''
    }
  }
}

db.save(views_vetcom)

views_notes = {
  "_id": "_design/notes",
  "views": {
    "none": {
      "map": '''function(doc) {
        if (!doc.notes) {
          emit(doc._id, doc) ;
        } 
      }'''
    },
    "not_trfrd": {
      "map": '''function(doc) {
        if (doc.vetcom && doc.notes && !doc.notes.trfrd) {
          emit(doc._id, doc) ;
        } 
      }'''
    }

  }
}

db.save(views_notes)
