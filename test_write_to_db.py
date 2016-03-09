#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('../LibraryWiki/')
import app.entity_iterators



if __name__ == "__main__":
    cl = pymongo.MongoClient()
    print(type(cl))
    db = cl['for_test']
    print(type(db))
    c = db.test_ents
    print(type(c))

    l = list(app.entity_iterators.get_authorities(from_id=0, to_id=3))
    c.insert(l[0])

    printf("docs in test_ents:", c.count())
