#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from elasticsearch import Elasticsearch


def parse_file_and_add_to_es(filename, es, index_name, id=0):
    with open(filename, "rb") as f:
        tree = etree.parse(f)

    for div in tree.xpath("//def:div[@LABEL]",
                          namespaces={'def': 'http://www.loc.gov/METS/'}):
        if div.get("TYPE") != "TEXT":
            continue
        chapter_div = div.getparent()
        while "CHAPTER" != chapter_div.get("TYPE"):
            chapter_div = chapter_div.getparent()
        # print(
        #    "CHAPTER ORDER:", chapter_div.get("ORDER"),
        #    "ORDER:", div.get("ORDER"),
        #    "LABEL:", div.get("LABEL")[:40]
        #    )
        es.index(index=index_name, doc_type="doc_test", id=id, body={
            "filename": filename,
            "chapter_order": chapter_div.get("ORDER"),
            "order:": div.get("ORDER"),
            "label:": div.get("LABEL"),
        })
        id += 1


if __name__ == "__main__":
    # parse_file_and_add_to_es("books_fmt/2704714-10-TEXT_utf8.xml")  # book in French
    # parse_file_and_add_to_es("books_fmt/2696068-10-TEXT_utf8.xml")  # book in English
    es = Elasticsearch()
    index_name = "books"
    es_count = es.count(index=index_name)['count']
    parse_file_and_add_to_es("books_fmt/1227225-140-TEXT_utf8.xml", es, index_name, es_count)  # book in Hebrew
