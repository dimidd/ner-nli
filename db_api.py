#! /usr/bin/python3
# coding=utf-8

import pymongo
import re

CL = pymongo.MongoClient()
DB = CL['ner-dict']
C = DB.ents


def lookup(alias):
    # as regex search in mongo is very slow, do a phrase search in mongo
    # and then a regex search only on the results
    alias_for_phrase_search = '\"{}\"'.format(alias)
    res = C.find({"$text": {"$search": alias_for_phrase_search}})

    alias_for_regex_search = r'^{}$'.format(alias)
    regex_alias = re.compile(alias_for_regex_search)
    good_matches = []
    for r in res:
        for a in r['aliases']:
            if regex_alias.match(a):
                good_matches.append(r)

    return good_matches


if __name__ == "__main__":
    print(C.count())
    t = lookup("יונתן בן עוזיאל")
    for r in t:
        print(r)
