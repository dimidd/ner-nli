from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entity(models.Model):
    class Types:
        PERSON = 1
        GEO = 2
        WORK = 3
        ORGANIZATION = 4
        MEETING = 5
        OTHER = 200

        choices = (
            (PERSON, _('Person')),
            (GEO, _('Geographic Place')),
            (WORK, _('Work')),
            (ORGANIZATION, _('Organization')),
            (MEETING, _('Meeting')),
            (OTHER, _('Other')),
        )
        codes = (
            ('geo', GEO),
            ('meet', MEETING),
            ('org', ORGANIZATION),
            ('work', WORK),
            ('other', OTHER),
        )
        from_code = dict(codes)
        to_code = dict([t[::-1] for t in codes])

    control_number = models.IntegerField(unique=True)
    type = models.IntegerField(choices=Types.choices, null=True, blank=True)
    aliases = models.TextField(null=True, blank=True)
    hebrew_alias = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.hebrew_alias

    def get_absolute_url(self):
        return reverse("entity_detail", args=(self.pk,))

    def type_code(self):
        return self.Types.to_code.get(self.type, 'unknown')
