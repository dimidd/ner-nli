#! /usr/bin/python3
# coding=utf-8

from elasticsearch import Elasticsearch
import requests
import json


if __name__ == "__main__":
    es = Elasticsearch()
    index_name = "books"
    # doc_type = "doc_test"

    mapping = {
        index_name: {
            "properties": {
                "filename": {
                    "type": "string",
                    "index": "not_analyzed",
                },
                "chapter_div": {
                    "type": "long",
                },
                "div": {
                    "type": "long",
                },
                "mets_type": {
                    "type": "string",
                    "index": "not_analyzed",
                },
                "label": {
                    "type": "string",
                    "analyzer": "english",  # hebrew?
                }
            },
        },
    }
    print("setting es index {} with mappings {}".format(
        index_name, json.dumps({"mappings": mapping})))
    r = requests.post('http://localhost:9200/{}/'.format(
        index_name), json.dumps({"mappings": mapping}))
    print(r.json())
