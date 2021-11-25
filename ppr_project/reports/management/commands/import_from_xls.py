from django.core.management.base import BaseCommand

from reports.parsers.xls_parser import (import_schedule_from_xls,
                                        import_objects_from_xls)


class Command(BaseCommand):
    help = 'Import maintenance schedule from xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='?', type=str)
        parser.add_argument('-o', '--objects', action='store_true')
        parser.add_argument('-s', '--schedules', action='store_true')

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']
        if kwargs['objects']:
            import_objects_from_xls(filepath)
        if kwargs['schedules']:
            import_schedule_from_xls(filepath)
