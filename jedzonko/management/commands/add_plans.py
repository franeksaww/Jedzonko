from django.core.management.base import BaseCommand
from random import randint

from jedzonko.models import Plan


class Command(BaseCommand):
    help = 'Tekst pomocy'

    def handle(self, *args, **options):
        for i in range(200):
            name = f'Przepis {i}'
            description = f'Opis {i}'
            Plan.objects.create(name=name, description=description)