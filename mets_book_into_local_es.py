#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from elasticsearch import Elasticsearch
import os


def parse_file_and_add_to_es(filename, es, index_name, id=0):
    with open(filename, "rb") as f:
        tree = etree.parse(f)

    for div in tree.xpath("//def:div[@LABEL]",
                          namespaces={'def': 'http://www.loc.gov/METS/'}):
        # chapter_div = div.getparent()
        # while "CHAPTER" != chapter_div.get("TYPE"):
        #     chapter_div = chapter_div.getparent()
        es.index(index=index_name, doc_type="doc_test", id=id, body={
            "filename": filename,
            # "chapter_div_id": chapter_div.get("ID"),
            "div_id": div.get("ID"),
            "label": div.get("LABEL"),
            "mets_type": div.get("TYPE"),
        })
        id += 1
    return id


if __name__ == "__main__":
    # parse_file_and_add_to_es("books_fmt/2704714-10-TEXT_utf8.xml")  # book in French
    # parse_file_and_add_to_es("books_fmt/2696068-10-TEXT_utf8.xml")  # book in English
    es = Elasticsearch()
    books_directory = "books_fmt"
    old_directory = os.getcwd()
    os.chdir(books_directory)
    index_name = "books"
    es_count = es.count(index=index_name)['count']
    id_count = parse_file_and_add_to_es("1227225-140-TEXT_utf8.xml", es, index_name, es_count)  # book in Hebrew
    print("indexed {} documents".format(id_count))
    os.chdir(old_directory)

