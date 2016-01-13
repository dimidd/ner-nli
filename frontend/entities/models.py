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
        from_code =  {
            'geo': GEO,
            'meet': MEETING,
            'org': ORGANIZATION,
            'work': WORK,
            'other': OTHER,
        }

    control_number = models.IntegerField(unique=True)
    type = models.IntegerField(choices=Types.choices, null=True, blank=True)
    aliases = models.TextField(null=True, blank=True)
    hebrew_alias = models.CharField(max_length=500, null=True, blank=True)
