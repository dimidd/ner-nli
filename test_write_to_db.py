#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('../LibraryWiki/')
import app.entity_iterators
import extract_ents
import pprint

if __name__ == "__main__":
    cl = pymongo.MongoClient()
    print(type(cl))
    db = cl['for_test']
    print(type(db))
    c = db.test_ents
    print(type(c))

    print("docs in test_ents:", c.count())

    # l = list(app.entity_iterators.get_authorities(from_id=72040, to_id=73860))
    l = list(app.entity_iterators.get_authorities(from_id=73854, to_id=73854))
    for item in l:
        #c.insert(extract_ents.extract_data_from_json_record(item.data))
        pprint.pprint(item.data)
        print('===========================')
        pprint.pprint(extract_ents.extract_data_from_entity_dict(item.data))

    print("docs in test_ents:", c.count())
