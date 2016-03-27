#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('../LibraryWiki/')
import app.entity_iterators
import pprint


if __name__ == "__main__":
    cl = pymongo.MongoClient()
    print(type(cl))
    db = cl['for_test']
    print(type(db))
    c = db.test_ents
    print(type(c))

    print("docs in test_ents:", c.count())

    l = list(c.find())
    for item in l:
        pprint.pprint(item)
        print()
    #c.remove({})

    print("docs in test_ents:", c.count())