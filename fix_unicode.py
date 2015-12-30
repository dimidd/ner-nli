#!/usr/bin/env python3
import pymongo

cl = pymongo.MongoClient()
db = cl['ner-dict']
old_c = db.dict
if 'ents' not in db.collection_names(False):
    db.create_collection('ents')
else:
    db.drop_collection('ents')
    db.create_collection('ents')
new_c = db.ents
qs = old_c.find()
for r in qs:
    new_aliases = []
    for a in r['aliases']:
        try:
            new_aliases.append(bytes(a, 'latin1').decode('utf8'))
        except UnicodeDecodeError:
            print(a)
            continue
    r['aliases'] = new_aliases
    new_c.insert_one(r)
