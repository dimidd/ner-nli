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


ranges ={}
for section_id in PARSE_NLI_DATA:
    ranges[section_id] = {}
    section_nlidata = PARSE_NLI_DATA[section_id]
    for keyword in section_nlidata:
        type = keyword[1]
        display_str = keyword[4][1]
        if display_str.find(' ') > -1:
            display = display_str.split()
        else:
            display = [display_str]
        ids = [[word['ID']] for word in keyword[5]]
        for i, word in enumerate(keyword[5]):
            ranges[section_id][word['ID']] = (ids, i, display[i], type)
