import os

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.now()

        with open(os.path.join(settings.MEDIA_ROOT, 'now.txt'), 'at') as f:
            time_str = f'Now: {timezone.localtime(now).strftime("%Y - %m - %d %H - %M - %S")}\n'
            f.write(time_str)
