from django.core.management.base import BaseCommand

from reports.parsers.xls_parser import import_from_xls


class Command(BaseCommand):
    help = 'Import maintenance schedule from xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to xlsx file')

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']
        import_from_xls(filepath)
