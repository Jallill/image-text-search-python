import shelve
db = shelve.open('data/imagesText')
for key in list(db.keys()):
    del db[key]
 
db.close()