# coding: utf-8

from django.shortcuts import render
from django.conf import settings
import os
from bs4 import BeautifulSoup
from dump108 import PARSE_NLI_DATA


def alto_section_list(request):
    pass

TYPE2COLOR = {
    'person': 'blue',
    'geo': 'green',
    'org': 'yellow',
    'meet': 'violet',
    'work': 'meet',
    'other': 'orange',
}



def alto_section(request, section_id='1227225-140-0108'):
    rang = ranges[section_id]
    xml_filename = os.path.join(
                    settings.BOOKS_DIR,
                    '%s.xml' % section_id
                    )
    bs = BeautifulSoup(open(xml_filename), "html.parser")
    # if xml contains multiple "Page" elements, it will only show the first one
    page = bs.alto.layout.page
    paragraphs = []
    paragraph = None
    line = None
    for printspace in page.findAll('printspace'):
        for textblock in printspace.findAll('textblock'):
            if paragraph is None:
                paragraph = {}
                paragraph['lines'] = []
                paragraph['class'] = 'reg'
            else:
                paragraphs.append(paragraph)
                paragraph = {}
                paragraph['lines'] = []
                paragraph['class'] = 'reg'
            for textline in textblock.findAll('textline'):
                if line is None:
                    line = []
                else:
                    paragraph['lines'].append(line)
                    line = []
                first = True
                for string in textline.findAll('string'):
                    if first and string:
                        if str(string).find('stylerefs') > -1:
                            if string['stylerefs'] == 'TXT_1':
                                line.append('</p> <p class="footnote" dir="rtl">')
                                paragraph['class'] = 'footnote'
                                first = False

                    if string['id'] in rang:
                        content = string['content']
                        tup = rang[string['id']]
                        ids, ind, aq, typ = tup
                        color = TYPE2COLOR[typ]
                        span_pre = u'<span style="color:{};">'.format(color)
                        span_suf = u'</span> '
                        html = aq
                        if ind == 0:
                            html = span_pre + aq
                        if ind == len(ids) - 1:
                            html += span_suf
                        line.append(html)
                    else:
                        line.append(u''+string['content']+u' ')
    paragraph['lines'].append(line)
    paragraphs.append(paragraph)

    return render(request, 'nernli/alto_section.html', context={
        'section_id': section_id,
        'xml_filename': xml_filename,
        'paragraphs': paragraphs,
        'nlidata': PARSE_NLI_DATA[section_id]
    })

PARSE_NLI_DATA= {
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
