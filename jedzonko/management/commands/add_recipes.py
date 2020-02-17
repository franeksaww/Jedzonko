from django.core.management.base import BaseCommand
from random import randint

from jedzonko.models import Recipe


class Command(BaseCommand):
    help = 'Tekst pomocy'

    def handle(self, *args, **options):
        for i in range(200):
            name = f'Przepis {i}'
            ingredients = f'Składnik {i}'
            description = f'Opis {i}'
            preparation_time = i
            Recipe.objects.create(name=name,
                                  ingredients=ingredients,
                                  description=description,
                                  preparation_time=preparation_time)