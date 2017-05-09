#!/usr/bin/env python3

from sickle import Sickle
from pprint import pprint
from lxml import etree, objectify
import xmltodict
import pymongo

import sys
sys.path.append('./LibraryWiki/')
import app.entity_iterators
import extract_ents
from app.node_entities import Authority

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
           'until': '2016-12-18T05:31:46Z',
          })
    return nli_records


def extract_data_from_oai_nli_record(record):
    pass


def convert_oai_file_to_marc21_dump(in_file_name, extracted_meta_file_name):
    with open(in_file_name, 'r') as in_file, \
         open(extracted_meta_file_name, 'w') as out_file:
        xml_header = ['<?xml version = "1.0" encoding = "UTF-8"?>',
                      '  <collection xmlns="http://www.loc.gov/MARC21/slim"',
                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                      'xsi:schemaLocation="http://www.loc.gov/MARC21/slim',
                      'http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">',
                      '']
        xml_end = ['',
                   '</collection>']
        xml_header = map(lambda l: l + '\n', xml_header)
        xml_end = map(lambda l: l + '\n', xml_end)

        out_file.writelines(xml_header)

        for line in in_file:
            example = etree.fromstring(line)
            ex_meta = example.find('{http://www.openarchives.org/OAI/2.0/}metadata')
            actual_record = list(ex_meta)[0]
            out_file.write(etree.tostring(actual_record, encoding='utf-8', pretty_print=True).decode('utf-8'))
        out_file.writelines(xml_end)


def test_update_db_from_sickle_xml_output_file(c):
    in_file_name = '/home/nelzas/for_nli/sample_output_from_sickle_script_as_is.xml'
    extracted_meta_file_name = '/home/nelzas/for_nli/extracted_meta_from_sickle_output.xml'

    convert_oai_file_to_marc21_dump(in_file_name, extracted_meta_file_name)

    print("docs in test_ents:", c.count())
    ents = app.entity_iterators.get_authorities(entities_file=extracted_meta_file_name, xml_prefix='marc:')  # all of them
    for item in ents:
        try:
            # print("in update_db - item:", item)
            ent_data = extract_ents.extract_data_from_entity_dict(item.data)
            if ent_data:
                # pprint(ent_data)
                # Do we need to look at the result from update_one?
                c.update_one(filter={"id": ent_data["id"]},
                        update={"$set": ent_data},
                             upsert=True)
        except Exception as e:
            print('exception from extract_data_from_entity_dict:', e)
            pprint(item.data)

    print("docs in test_ents:", c.count())


def xml_record_2_authority(record_str, xml_prefix=''):
    '''convert an xml string received received from sickle

    code copied and adapted from LibraryWiki's get_authorities function
    '''
    parsed_buf = xmltodict.parse(record_str, process_namespaces=False)
    parsed_buf = parsed_buf['record']['metadata']
    prefixed_record_str = '{xml_prefix}record'.format(xml_prefix=xml_prefix)
    record = parsed_buf[prefixed_record_str]
    result = {k: record[k] for k in record if
            k == "{xml_prefix}controlfield".format(xml_prefix=xml_prefix) or
            k == "{xml_prefix}datafield".format(xml_prefix=xml_prefix)}
    if result.get('{xml_prefix}datafield'.format(xml_prefix=xml_prefix)):
        return Authority(app.authorities.convert_dict(result, xml_prefix))
    else:
        return None


if __name__ == "__main__":

    cl = pymongo.MongoClient('localhost', 27017)  # default port!
    db = cl['for_test']
    c = db.test_ents

    #test_update_db_from_sickle_xml_output_file(c)

    nli_records = get_some_records()

    # this prefix appears in the results from NLI OAI queries
    # and we need to remove it from the string to get the actual ID
    ID_PREFIX = 'oai:aleph-nli:NNL10-'
    for i, r in enumerate(nli_records):
        print('processing record: ', i)
        if r.deleted:
            raw_id = r.header.identifier
            assert raw_id.startswith(ID_PREFIX)
            r_id = int(raw_id[len(ID_PREFIX):])
            print('deleting: ', r_id)
            c.remove({'id': {"$eq": r_id}})
        else:  # update or create new record
            # print(i, r.header)
            # print('r.raw:', r.raw)
            # record_as_dict = xmltodict.parse(r.raw, process_namespaces=False)
            # print('res from xmltodict:', record_as_dict)
            # print("record_as_dict['record']['metadata']:", record_as_dict['record']['metadata'])
            ent = xml_record_2_authority(r.raw, xml_prefix='marc:')
            # print(ent)
            try:
                # print("in update_db - ent.data:", ent.data)
                ent_data = extract_ents.extract_data_from_entity_dict(ent.data)
                if ent_data:
                    # pprint(ent_data)
                    # Do we need to look at the result from update_one?
                    c.update_one(filter={"id": ent_data["id"]},
                            update={"$set": ent_data},
                                 upsert=True)
            except Exception as e:
                print('exception from extract_data_from_entity_dict:', e)
                pprint(ent.data)
