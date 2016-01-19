from django.views.generic import ListView, DetailView

from . import models


class EntityListView(ListView):
    model = models.Entity


class EntityDetailView(DetailView):
    model = models.Entity
