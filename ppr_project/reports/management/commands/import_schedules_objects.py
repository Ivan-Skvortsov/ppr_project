from django.core.management.base import BaseCommand

from reports.parsers.xls_parser import execute_import_schedules_and_objects


class Command(BaseCommand):
    help = 'Import maintenance schedule from xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='?', type=str)

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']
        execute_import_schedules_and_objects(filepath)
