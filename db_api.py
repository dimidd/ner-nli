import pymongo

CL = pymongo.MongoClient()
DB = CL['ner-dict']
C = DB.ents


def lookup(alias):
    res = C.find_one({"$text": {"$search": alias}})

    return res
