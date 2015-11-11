#! /usr/bin/python3
# coding=utf-8

from lxml import etree


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
        words.append({"ID:": word.get("ID"),
                      "CONTENT:": word.get("CONTENT"),
                      "parent:": word.getparent().get("ID"),
                      })
    return words


if __name__ == "__main__":
    print(extract_words_from_alto_xml("books_alto_fmt/1227225-140-0100.xml"))
