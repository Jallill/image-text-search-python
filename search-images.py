from re import X
import shelve

db = shelve.open('data/imagesText')

searchText = input('Texto a buscar ')
found = []
for key in list(db.keys()):
    if len((list(filter(lambda text: searchText in text, db[key])))) > 0:
        found.append(key)

for file in found:
    print(file)

db.close()