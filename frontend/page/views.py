from django.shortcuts import render
from django.conf import settings
import os


def alto_section(request, section_id):
    xml_filename = os.path.join(settings.DATA_DIR, 'alto_section_xmls', '%s.xml'%section_id)

    return render(request, 'nernli/alto_section.html', context={
        'section_id': section_id,
        'xml_filename': xml_filename,
    })
