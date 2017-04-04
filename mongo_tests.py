#!/usr/bin/env python3
import pymongo
import sys
sys.path.append('./LibraryWiki/')
import app.entity_iterators
from pprint import pprint


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

    # l = c.find()

    #for i in l:
    #    print(i['id'])

    #alias = "יונתן בן עוזיאל"
    alias = "Bet ḥolim Alin"
    alias_for_phrase_search = '\"{}\"'.format(alias)

    #res = db.command('text', 'test_ents', search='בן')
    #res = db.command('text', 'test_ents', search=alias_for_phrase_search)
    res = c.find({"$text": {"$search": "Hospital"}})
    #res = c.find({"$text": {"$search": alias_for_phrase_search}})
    #print(type(res))
    #pprint(res)
    #print()
    #pprint(res['results'])
    for i in res:
        pprint(i)

    # c.remove({})

    print("docs in test_ents:", c.count())
