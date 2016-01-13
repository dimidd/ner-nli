#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from pathlib import Path
import sys


def extract_words_from_alto_xml(filepath):
    """
    extract words from an xml file in alto format
    return list of words, each word is accompanied with metadata
    to locate its source

    """
    with filepath.open() as f:
        tree = etree.parse(f)
    res = []
    for word in tree.xpath("//String[@CONTENT]"):
        res.append(word.get("CONTENT"))

    print(' '.join(res))


def gather_info_from_folder(path, file):
    if file:
        extract_words_from_alto_xml(Path(file))
        return

    folder = Path(path)
    l = list(folder.glob('*.xml'))
    l = sorted(l)
    for f in l:
        extract_words_from_alto_xml(f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = None
    path = "../nli_entities_sample_data/additional_books/IE26721743/REP26723234/"
    gather_info_from_folder(path, file)
