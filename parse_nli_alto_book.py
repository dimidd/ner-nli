#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from pprint import pprint


def extract_words_from_alto_xml(filename):
    """
    extract words from an xml file in alto format
    return list of words, each word is accompanied with metadata
    to locate its source

    """
    with open(filename, "rb") as f:
        tree = etree.parse(f)
    words = []
    for word in tree.xpath("//String[@CONTENT]"):
        words.append({"ID": word.get("ID"),
                      "CONTENT": word.get("CONTENT"),
                      "PARENT": word.getparent().get("ID"),
                      })
    return words


def lookup(candidate, entities):
    """
        return first record in entities that match candidate
    """
    for record in entities:
        if candidate == record['name']:
            return record['id']
    return None


def slice(l, size):
    for i in range(len(l) + 1 - size):
        yield l[i:i+size]


def candidate2text(candidate):
    return ", ".join([w['CONTENT'] for w in candidate])


def generate_candidate_variants(candidate):
    candidate_as_str = candidate2text(candidate)
    yield candidate_as_str


def look_for_entities(words, entities):
    res = []
    for candidate in slice(words, 2):
        for candidate_as_str in generate_candidate_variants(candidate):
            t = lookup(candidate_as_str, entities)
            if t:
                res.append((t, candidate, candidate_as_str))
    return res

if __name__ == "__main__":
    words = extract_words_from_alto_xml("books_alto_fmt/1227225-140-0100.xml")
    entities = [
        {'id': 1, 'name': 'לחוק, התורהl', },
        {'id': 2, 'name': 'חייבים, לשמוע', },
        {'id': 3, 'name': 'ישראל, בניגוד', },
        {'id': 4, 'name': 'לחוק, בניגוד', },
        ]
    # TODO probably send source (name of file which contains page?) also
    res = look_for_entities(words, entities)
    pprint(res)
