#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions
import os
import json

def parse_file_and_add_to_es(filename, es, index_name, id=0):
    # ensure we won't enter same file again with new ids
    query = {"match": {"filename": filename}}
    r = es.search(index=index_name,
                  doc_type="mets_paragraph",
                  body=json.dumps({"query": query}))
    num_of_results = r['hits']['total']
    if num_of_results > 0:
        return 0

    with open(filename, "rb") as f:
        tree = etree.parse(f)

    count = 0
    for div in tree.xpath("//def:div[@LABEL]",
                          namespaces={'def': 'http://www.loc.gov/METS/'}):
        # chapter_div = div.getparent()
        # while "CHAPTER" != chapter_div.get("TYPE"):
        #     chapter_div = chapter_div.getparent()
        es.index(index=index_name, doc_type="mets_paragraph", id=(id+count), body={
            "filename": filename,
            # "chapter_div_id": chapter_div.get("ID"),
            "div_id": div.get("ID"),
            "label": div.get("LABEL"),
            "mets_type": div.get("TYPE"),
        })
        count += 1
    return count


if __name__ == "__main__":
    # parse_file_and_add_to_es("books_fmt/2704714-10-TEXT_utf8.xml")  # book in French
    # parse_file_and_add_to_es("books_fmt/2696068-10-TEXT_utf8.xml")  # book in English
    es = Elasticsearch()
    books_directory = "books_fmt"
    old_directory = os.getcwd()
    os.chdir(books_directory)
    index_name = "books"
    books = [
        "1227225-140-TEXT_utf8.xml",
        "2328559-10-TEXT_utf8.xml",
        "1088674-10-TEXT_utf8.xml",
        "001162278-TEXT_utf8.xml",
    ]
    try:
        es_count = es.count(index=index_name)['count']
    except es_exceptions.NotFoundError:
        es_count = 0
    id_count = 0
    for book in books:
        id_count = parse_file_and_add_to_es(book, es, index_name, es_count)  # book in Hebrew
        print("indexed {} documents from {}".format(id_count, book))
        es_count += id_count
    os.chdir(old_directory)
