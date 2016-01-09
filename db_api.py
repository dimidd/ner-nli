#! /usr/bin/python3
# coding=utf-8

import pymongo
import re

CL = pymongo.MongoClient()
DB = CL['ner-dict']
C = DB.ents

# improve: if no result found try to remove the following prefixes:
# ו, ל, מ, ב, כ, ש,
# ול, ומ, וב, וכ, וש,
# של, שמ, שב, שכ,
# כש, וכש, שכש, לכש, ולכש,
# ה, וה, מה, שה, ומה, ושה, כשה, וכשה, לכשה, ולכשה, ומש, ומשה,
# and lookup again...

def lookup(alias):
    # as regex search in mongo is very slow, do a phrase search in mongo
    # and then a regex search only on the results
    alias_for_phrase_search = '\"{}\"'.format(alias)
    res = C.find({"$text": {"$search": alias_for_phrase_search}})

    alias_for_regex_search = r'^{}$'.format(alias)
    try:
        regex_alias = re.compile(alias_for_regex_search)
    except:
        print("problem with: '{}'!".format(alias))
        return []
    good_matches = []
    for r in res:
        if r['type'] == 'other':
            continue
        for a in r['aliases']:
            if regex_alias.match(a):
                good_matches.append(r)

    return good_matches


if __name__ == "__main__":
    print(C.count())
    t = lookup("יונתן בן עוזיאל")
    for r in t:
        print(r)
