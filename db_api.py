#! /usr/bin/python3
# coding=utf-8

import pymongo
import re

#CL = pymongo.MongoClient()
CL = pymongo.MongoClient('localhost', 29017)  # not default port!
#DB = CL['ner-dict']
#C = DB.ents
DB = CL['for_test']
C = DB.test_ents

# improve: if no result found try to remove the following prefixes:
# ו, ל, מ, ב, כ, ש,
# ול, ומ, וב, וכ, וש,
# של, שמ, שב, שכ,
# כש, וכש, שכש, לכש, ולכש,
# ה, וה, מה, שה, ומה, ושה, כשה, וכשה, לכשה, ולכשה, ומש, ומשה,
# and lookup again...


def lookup(alias, no_other=True):
    # as regex search in mongo is very slow, do a phrase search in mongo
    # and then a regex search only on the results
    alias_for_phrase_search = '\"{}\"'.format(alias)
    #res = C.find({"$text": {"$search": alias_for_phrase_search}})
    #res = C.find({"text": {"search": alias_for_phrase_search}})
    res = DB.command('text', 'test_ents', search=alias_for_phrase_search)

    alias_regex_str = r'^{}[.,]?$'.format(alias)
    geo_regex_str = r'^{} \(.+\)$'.format(alias)
    try:
        alias_regex = re.compile(alias_regex_str)
        geo_regex = re.compile(geo_regex_str)
    except:
        print("problem with: '{}'!".format(alias))
        return []
    good_matches = []
    for r in res['results']:
        r = r['obj']
        try:
            if r['type'] == 'other':
                continue
        except KeyError as e:
            print("exception:", e)
            print("query:", alias_for_phrase_search)
            print("type of r:", type(r))
            print("r:", r)
        for a in r['aliases']:
            if alias_regex.match(a):
                good_matches.append(r)
            if geo_regex.match(a) and r['type'] == 'geo':
                good_matches.append(r)

    return good_matches


if __name__ == "__main__":
    print(C.count())
    t = lookup("יונתן בן עוזיאל")
    for r in t:
        print(r)
