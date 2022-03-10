from django.core.management.base import BaseCommand

from reports.parsers.xls_parser import execute_import_templates


class Command(BaseCommand):
    help = 'Import docx templates from xlsx file and updates schedules'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='?', type=str)

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']
        execute_import_templates(filepath)
