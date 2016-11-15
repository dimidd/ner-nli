#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('./LibraryWiki/')
import app.entity_iterators
import extract_ents
import pprint

if __name__ == "__main__":
    cl = pymongo.MongoClient('localhost', 27017)  # default port!
    print(type(cl))
    db = cl['for_test']
    print(type(db))
    c = db.test_ents
    print(type(c))

    print("docs in test_ents:", c.count())

    entities_file = "/home/nelzas/for_nli/nnl10_dump_20_03_2016.xml"

    #ents = app.entity_iterators.get_authorities(from_id=72000, to_id=75000, entities_file=entities_file)
    ents = app.entity_iterators.get_authorities(to_id=500, entities_file=entities_file)
    #ents = app.entity_iterators.get_authorities(entities_file=entities_file)  # all of them
    #for item in l:
    for item in ents:
        #c.insert(extract_ents.extract_data_from_json_record(item.data))
        #pprint.pprint(item.data)
        #print('===========================')
        #pprint.pprint(extract_ents.extract_data_from_entity_dict(item.data))
        try:
            ent_data = extract_ents.extract_data_from_entity_dict(item.data)
            if ent_data:
                c.insert(ent_data)
        except Exception as e:
            print('exception from extract_data_from_entity_dict:', e)
            pprint.pprint(item.data)

    print("docs in test_ents:", c.count())
