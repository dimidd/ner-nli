#!/usr/bin/env python3
import pymongo
import copy

cl = pymongo.MongoClient()
db = cl['ner-dict']
c = db.ents
qs = c.find()

for r in qs:
    aliases = [a.replace(',', '') for a in r['aliases']]
    r2 = copy.deepcopy(r)
    r2['aliases'] = aliases
    c.update_one({"_id": r['_id']}, {"$set": r2})
