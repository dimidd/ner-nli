#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('./LibraryWiki/')
import app.entity_iterators
from pprint import pprint
from datetime import datetime

import json

if __name__ == "__main__":
    cl = pymongo.MongoClient('localhost', 27017)  # default port!
    #print(type(cl))
    db = cl['for_test']
    #print(type(db))
    c = db.test_ents
    #print(type(c))

    #print("docs in test_ents:", c.count())

    c.create_index([('primary_aliases', pymongo.TEXT), ('secondary_aliases', pymongo.TEXT)], name='aliases_text', default_language='none')
    #print(c.index_information())

    #l = c.find().sort('_id', pymongo.ASCENDING)

    #for i in l:
    #    print(i['_id'], i['id'])

    #alias = "יונתן בן עוזיאל"
    alias = "Bet ḥolim Alin"
    alias_for_phrase_search = '\"{}\"'.format(alias)

    #res = db.command('text', 'test_ents', search='בן')
    #res = db.command('text', 'test_ents', search=alias_for_phrase_search)
    #res = c.find({"$text": {"$search": "Hospital"}})
    #res = c.find({"$text": {"$search": alias_for_phrase_search}})
    #res = c.find({'id': {"$eq": 4198335}})
    #res = c.find({
    #        'type': {"$eq": "geo"},
    #        '$or': [{'primary_aliases': {'$regex': '[א-ת]'}},
    #                {'secondary_aliases': {'$regex': '[א-ת]'}},
    #                ]
    #    },
    #    limit=10)
    #print(type(res))
    #pprint(res)
    #print()
    #pprint(res['results'])
    #for i in res:
    #    pprint(i)
    search_geo_heb = {
            'type': {"$eq": "geo"},
            '$or': [{'primary_aliases': {'$regex': '[א-ת]'}},
                    {'secondary_aliases': {'$regex': '[א-ת]'}},
                    ]
        }
    with open('geo_heb.json', 'w') as f:
        f.write('[')
        for obj in c.find(search_geo_heb):
            del obj['_id']
            json.dump(obj, f, indent=2)
            f.write(',')
#        json.dump(list_of_dicts[-1], f)
        f.write(']')
    #for i in c.find(search_geo_heb):
        #print(type(i))
        #pprint(i)

    # c.remove({'id': {"$eq": 2341151}})
    # c.remove({})

    print("docs in test_ents:", c.count())

    m = db.meta_test_ents
    #d = m.find_one()
    #print(d)
    #m.insert_one({'last_update': None})
    d = m.find_one({'last_update':{'$exists': True}})
    print(d)
    #m.update_one(filter={'last_update':{'$exists': True}},
    #             update={
    #                 "$currentDate": {
    #                     "lastModified": {
    #                         "$type": "date"
    #                         }
    #                     },
    #                 "$set": {
    #                     'last_update': '2017-10-17T20:13:44Z',
    #                     }
    #                    },
    #             upsert = True)
    #d = m.find_one({'last_update':{'$exists': True}})
    #print(d)
    #print(d['lastModified'].isoformat())
    #print(d['lastModified'].date())
    # m.update_one(filter={'last_update':{'$exists': True}},
    #              update={
    #                 "$set": {
    #                     'last_update': None,
    #                     "lastModified": datetime(2016, 6, 6, 0, 0),
    #                     }
    #                 },
    #              upsert = True)
    # d = m.find_one({'last_update':{'$exists': True}})
    # print(d)
    # print(d['lastModified'].isoformat())
    # print(d['lastModified'].date())
    #m.remove({})
