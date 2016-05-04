#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('../LibraryWiki/')
import app.entity_iterators
import extract_ents
import pprint

if __name__ == "__main__":
    cl = pymongo.MongoClient('localhost', 29017)  # not default port!
    print(type(cl))
    db = cl['for_test']
    print(type(db))
    c = db.test_ents
    print(type(c))

    print("docs in test_ents:", c.count())

    # l = list(app.entity_iterators.get_authorities(from_id=72040, to_id=73860))
    #l = list(app.entity_iterators.get_authorities(from_id=72049, to_id=72049))
    #ents = app.entity_iterators.get_authorities(from_id=70000, to_id=80000)
    ents = app.entity_iterators.get_authorities()  # all of them
    #for item in l:
    for item in ents:
        #c.insert(extract_ents.extract_data_from_json_record(item.data))
        #pprint.pprint(item.data)
        #print('===========================')
        #pprint.pprint(extract_ents.extract_data_from_entity_dict(item.data))
        try:
            c.insert(extract_ents.extract_data_from_entity_dict(item.data))
        except Exception as e:
            print('exception:', e)
            pprint.pprint(item.data)

    print("docs in test_ents:", c.count())
