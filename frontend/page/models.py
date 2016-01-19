import json

import os.path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from entities.models import Entity


class Book(models.Model):
    title = models.CharField(max_length=500)
    path = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=(self.pk,))


class Page(models.Model):
    book = models.ForeignKey(Book, related_name='pages')
    ordinal = models.IntegerField()
    path = models.CharField(max_length=500)

    class Meta:
        unique_together = (
            ('book', 'ordinal'),
            ('book', 'path'),
        )

    def __str__(self):
        return "{} עמ' {}".format(self.book, self.ordinal)

    def get_absolute_url(self):
        return reverse("page_detail", args=(self.pk,))

    def file_path(self):
        return os.path.join(self.book.path, "{}.xml".format(self.path))

    def full_file_path(self):
        return os.path.join(settings.DATA_DIR, self.file_path())

    def all_keywords(self):
        return {id: hit for hit in self.hits.all() for id in hit.keywords()}


class Hit(models.Model):
    entity = models.ForeignKey(Entity, related_name='hits')
    page = models.ForeignKey(Page, related_name='hits')
    content = models.CharField(max_length=500)
    first_word_id = models.CharField(max_length=500)
    word_count = models.IntegerField()
    lookup_used = models.CharField(max_length=500)

    alto_info = models.TextField()
    """
        list of:
            word_id
            content
            block_id?
            hpos?
            vpos?
            width?
            wc?
            cc?
    """

    class Meta:
        unique_together = (
            ('page', 'first_word_id'),
        )

    def get_alto_info(self):
        return json.loads(self.alto_info)

    def keywords(self):
        return {word['id'] for word in self.get_alto_info()}
