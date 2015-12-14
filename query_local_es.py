#! /usr/bin/python3
# coding=utf-8

from elasticsearch import Elasticsearch

if __name__ == "__main__":
    es = Elasticsearch()
    index_name = "books"
    es_count = es.count(index=index_name)['count']
    print(es_count)
    es_count = 1
    for i in range(es_count):
        print(es.get(index=index_name, doc_type="mets_paragraph", id=i))
        # es.delete(index=index_name, doc_type="mets_paragraph", id=i)
