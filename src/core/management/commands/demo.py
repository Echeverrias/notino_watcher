from django.core.management.base import BaseCommand, CommandError

import logging
logging.getLogger().setLevel(logging.INFO)

class Command(BaseCommand):
    help = "Demo"

    def handle(self, *args, **options):

        print('DEMO..')