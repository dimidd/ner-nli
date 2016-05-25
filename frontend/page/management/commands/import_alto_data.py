import json
import os.path
from glob import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from page.importer import import_result


class Command(BaseCommand):
    help = 'Add some scratch data to the DB'

    def handle(self, *args, **options):
        pattern = os.path.join(settings.BASE_DIR, "data", "*.json")
        for fn in glob(pattern):
            print(fn, end=": ")
            with open(fn) as f:
                base = os.path.splitext(os.path.basename(fn))[0]
                n = 0
                for result in json.load(f):
                    n += import_result(base, *result)
        print(n)
