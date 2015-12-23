#! /usr/bin/python3
# coding=utf-8

import pymongo

CL = pymongo.MongoClient()
DB = CL['ner-dict']
C = DB.ents


def lookup(alias):
    alias_for_phrase_search = '\"{}\"'.format(alias)
    res = C.find_one({"$text": {"$search": alias_for_phrase_search}})

    return res


if __name__ == "__main__":
    print(C.count())
    print(lookup("Leon Pol"))
