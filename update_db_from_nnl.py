#!/usr/bin/env python3

from sickle import Sickle
from pprint import pprint

if __name__ == "__main__":
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
           'until': '2016-12-18T05:31:45Z',
          })
    for item in nli_records:
        print(item)
    print()

