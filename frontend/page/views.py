from django.shortcuts import render
from django.conf import settings
import os
from bs4 import BeautifulSoup


def alto_section(request, section_id):
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
                    line.append(string['content'])
    paragraph.append(line)
    paragraphs.append(paragraph)

    return render(request, 'nernli/alto_section.html', context={
        'section_id': section_id,
        'xml_filename': xml_filename,
        'paragraphs': paragraphs,
    })




