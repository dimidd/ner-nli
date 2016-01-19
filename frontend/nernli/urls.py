from django.conf.urls import url
from django.contrib import admin

import entities.views
import page.views

urlpatterns = [

    url(r'^$', page.views.BookListView.as_view(), name="book_list"),

    url(r'^book/(?P<pk>\d+)/$', page.views.BookDetailView.as_view(),
        name="book_detail"),

    url(r'^page/(?P<pk>\d+)/$', page.views.PageDetailView.as_view(),
        name="page_detail"),

    url(r'^entity/$', entities.views.EntityListView.as_view(),
        name="entity_list"),

    url(r'^entity/(?P<pk>\d+)/$', entities.views.EntityDetailView.as_view(),
        name="entity_detail"),

    url(r'^admin/', admin.site.urls),
]
