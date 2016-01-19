# coding: utf-8

from django.views.generic import ListView, DetailView

from page import alto_tools
from . import models


class BookListView(ListView):
    model = models.Book


class BookDetailView(DetailView):
    model = models.Book


class PageDetailView(DetailView):
    model = models.Page

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)

        page = self.object

        paragraphs = alto_tools.get_paragraphs(page.full_file_path(),
                                               page.all_keywords())

        d.update({
            'xml_filename': page.full_file_path(),
            'paragraphs': paragraphs,
        })

        return d
