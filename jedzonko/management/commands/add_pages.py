from django.core.management.base import BaseCommand
from random import randint

from jedzonko.models import Page


class Command(BaseCommand):
    help = 'Tekst pomocy'

    def handle(self, *args, **options):
        Page.objects.create(title='about', description='Reaalllllyyy', slug='/about/')
        Page.objects.create(title='contact', description='Dosynt meter', slug='/contact/')
