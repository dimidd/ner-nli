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


def lookup(word, entities):
    """
        return first record in entities that match word
    """
    for record in entities:
        if word == record['name']:
            return record['id']
    return None


def slice(l, size):
    for i in range(len(l) + 1 - size):
        yield l[i:i+size]


def candidate2text(candidate):
    return " ".join([w['CONTENT'] for w in candidate])


def look_for_entities(words, entities):
    res = []
    for candidate in slice(words, 2):
        t = lookup(candidate2text(candidate), entities)
        if t:
            res.append((t, candidate))
    return res

if __name__ == "__main__":
    words = extract_words_from_alto_xml("books_alto_fmt/1227225-140-0100.xml")
    entities = [
        {'id': 1, 'name': 'חייבים לשמוע', },
        {'id': 2, 'name': 'ישראל בניגוד', },
        {'id': 2, 'name': 'לחוק התורהl', },
        ]
    # TODO probably send source (name of file which contains page?) also
    res = look_for_entities(words, entities)
    pprint(res)
