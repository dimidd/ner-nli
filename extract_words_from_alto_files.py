#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from pprint import pprint
from pathlib import Path


def extract_words_from_alto_xml(filepath):
    """
    extract words from an xml file in alto format
    return list of words, each word is accompanied with metadata
    to locate its source

    """
    with filepath.open() as f:
        tree = etree.parse(f)
    for word in tree.xpath("//String[@CONTENT]"):
        print(word.get("CONTENT"))


def gather_info_from_folder(path):
    folder = Path(path)
    l = list(folder.glob('*.xml'))
    l = sorted(l)
    for f in l:
        extract_words_from_alto_xml(f)


if __name__ == "__main__":
    path = "../nli_entities_sample_data/additional_books/IE26721743/REP26723234/"
    gather_info_from_folder(path)
