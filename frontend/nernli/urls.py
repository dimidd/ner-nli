from django.conf.urls import url
from django.contrib import admin
from page import views as page_views

urlpatterns = [

    url(r'^$', page_views.page),
    url(r'^alto-section/$', page_views.alto_section_list),
    url(r'^alto-section/(?P<section_id>\d+)$', page_views.page),
    url(r'^alto-section/(\d+)/$', page_views.page),

    url(r'^admin/', admin.site.urls),
]
