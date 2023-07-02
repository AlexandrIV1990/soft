from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from image.models import Image
from image.services import CreateImageDB


class Command(BaseCommand):
    help = 'Команда для парсинга csv'

    def handle(self, *args, **options):
        self.parse_csv(options)

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--clear_db',
            action='store_true',
            default=False,
            help='Очистить базу данных'
        )
        parser.add_argument(
            '-p',
            '--path',
            default=settings.PATH_CSV,
            help='первая часть названия'
        )

    @atomic
    def parse_csv(self, options):
        if options['clear_db']:
            Image.objects.all().delete()
        CreateImageDB(options['path']).execute()
