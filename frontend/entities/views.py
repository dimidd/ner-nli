from django.views.generic import ListView, DetailView

from . import models


class EntityListView(ListView):
    model = models.Entity


class EntityDetailView(DetailView):
    model = models.Entity


class EntityTooltipView(DetailView):
    template_name = "entities/entity_tooltip.html"
    model = models.Entity
