# coding: utf-8

from django.shortcuts import render, get_object_or_404

from page import alto_tools
from . import models


def alto_section_list(request):
    pass


def page(request, pk):
    page = get_object_or_404(models.Page, id=pk)

    paragraphs = alto_tools.get_paragraphs(
            page.full_file_path(),
            page.all_keywords()
    )

    return render(request, 'nernli/alto_section.html', {
        'section_id': pk,
        'xml_filename': page.full_file_path(),
        'paragraphs': paragraphs,
    })
