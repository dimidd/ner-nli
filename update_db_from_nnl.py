#!/usr/bin/env python3

from sickle import Sickle
from pprint import pprint
from lxml import etree, objectify

def get_some_records():
    """Example from Eyal's mail:
       http://aleph.nli.org.il/OAI?verb=ListRecords&metadataprefix=marc21&set=AUTREIMRC"""

    sickle = Sickle('http://aleph.nli.org.il/OAI')
    nli_identify = sickle.Identify()
    # print(type(nli_identify))
    # print(nli_identify)
    #for item in nli_identify:
    #    print(item)
    #print()
    #nli_sets = sickle.ListSets()
    # print(type(nli_sets))
    # print(nli_sets)
    #for item in nli_sets:
    #    print(item)
    #print()

    # record = sickle.GetRecord(identifier="001891756", metadataprefix="marc21")
    # record = sickle.GetRecord(metadataprefix='marc21', identifier='oai:aleph-nli:NNL10-002131482')
    # print(type(record))

    nli_records = sickle.ListRecords(
        **{'metadataprefix': 'marc21',
           'set': 'AUTREIMRC',
           'from': '2016-12-18T05:31:45Z',
           'until': '2016-12-19T05:31:45Z',
          })
    return nli_records


def extract_data_from_oai_nli_record(record):
    pass


if __name__ == "__main__":
    #nli_records = get_some_records()
    nli_records = []
    with open('/home/nelzas/for_nli/sample_output_from_sickle_script_as_is.xml', 'r') as f:
        for line in f:
            nli_records.append(line)


    for item in nli_records:
        print(item)
#        record = objectify.fromstring(item)
#        print(dir(record))
#        print(record)
#        pprint(record.keys())
        example = etree.fromstring(item)
        print("attrib:")
        pprint(example.attrib)
        print("getchildren:")
        pprint(example.getchildren())
        for c in example.getchildren():
            print("in child")
            print(c)
            print("in child getchildren:")
            pprint(c.getchildren())
            for cc in c.getchildren():
                print("cc")
                pprint(cc)
                pprint(cc.getchildren())
            #print(dir(c))
            #print(c.items())
        #pprint(example.xpath(u'//metadata',
        #                     namespaces={'def': 'http://www.openarchives.org/OAI/2.0/'}))
    print()
