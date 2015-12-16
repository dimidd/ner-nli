# coding: utf-8

from django.shortcuts import render
from django.conf import settings
import os
from bs4 import BeautifulSoup


def alto_section(request, section_id='1227225-140-0100'):
    highlight_ids = HIGHLIGHT_IDS[section_id]
    xml_filename = os.path.join(settings.DATA_DIR, 'alto_section_xmls', '%s.xml'%section_id)
    bs=BeautifulSoup(open(xml_filename), "html.parser")
    # if xml contains multiple "Page" elements, it will only show the first one
    page = bs.alto.layout.page
    paragraphs = []
    paragraph = None
    line = None
    for printspace in page.findAll('printspace'):
        for textblock in printspace.findAll('textblock'):
            if paragraph is None:
                paragraph = []
            else:
                paragraphs.append(paragraph)
                paragraph = []
            for textline in textblock.findAll('textline'):
                if line is None:
                    line = []
                else:
                    paragraph.append(line)
                    line = []
                for string in textline.findAll('string'):
                    if string['id'] in highlight_ids:
                        line.append(u'<span style="color:red;">'+string['content']+u'</span> ')
                    else:
                        line.append(u''+string['content']+u' ')
    paragraph.append(line)
    paragraphs.append(paragraph)

    return render(request, 'nernli/alto_section.html', context={
        'section_id': section_id,
        'xml_filename': xml_filename,
        'paragraphs': paragraphs,
        'nlidata': PARSE_NLI_DATA[section_id]
    })


PARSE_NLI_DATA = {
    '1227225-140-0100': [(2,
      [{'CONTENT': 'חייבים',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00009',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00001'},
       {'CONTENT': 'לשמוע',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00010',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00001'}],
      'חייבים לשמוע'),
     (3,
      [{'CONTENT': 'ישראל',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00241',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00023'},
       {'CONTENT': 'בניגוד',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00242',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00023'}],
      'ישראל בניגוד'),
     (4,
      [{'CONTENT': 'בניגוד',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00242',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00023'},
       {'CONTENT': 'לחוק',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00243',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00023'}],
      'לחוק בניגוד'),
     (1,
      [{'CONTENT': 'לחוק',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00243',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00023'},
       {'CONTENT': 'התורהl',
        'GRANDPARENT': 'P100_TB00001',
        'ID': 'P100_ST00244',
        # 'PAGE_FILE': PosixPath('books2/IE26721743/REP26723234/1227225-140-0100.xml'),
        'PARENT': 'P100_TL00024'}],
      'לחוק התורהl')]

}

HIGHLIGHT_IDS = {}
for section_id in PARSE_NLI_DATA:
    HIGHLIGHT_IDS[section_id] = []
    section_nlidata = PARSE_NLI_DATA[section_id]
    for keyword in section_nlidata:
        for word in keyword[1]:
            HIGHLIGHT_IDS[section_id].append(word['ID'])
