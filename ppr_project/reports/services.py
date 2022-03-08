from collections import defaultdict
from datetime import datetime
from docxtpl import DocxTemplate
from pathlib import Path

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date as _date

import reports.constants as constants
from reports.models import Schedule


class DocxReportGenerator:
    """Generate docx reports."""

    def __init__(self, schedule_id):
        self.schedule = get_object_or_404(Schedule, id=schedule_id)

    def _get_context_for_docx_report(self):
        """Generate context from Schedule object to render docx report."""
        return {
            'facility_name':
                self.schedule.equipment_type.facility.facility_name,
            'day': self.schedule.date_completed.day,
            'month': _date(self.schedule.date_completed, 'E'),
            'year': self.schedule.date_completed.year,
            'sched_year': constants.SHEDULE_YEAR,
            'shed_date_utv': constants.SHEDULE_DATE_APPROVED,
            'remarks': None,  # TODO: add remarks to schedule model
            'employee1': self.schedule.employee1.position,
            'employee2': self.schedule.employee2.position,
            'employee3': self.schedule.employee3.position
                if self.schedule.employee3 else None,
            'name1': self.schedule.employee1.name,
            'name2': self.schedule.employee2.name,
            'name3': self.schedule.employee3.name
                if self.schedule.employee3 else None
        }

    def _get_docx_report_template(self):
        """Gets template for docx report."""
        return settings.MEDIA_ROOT / str(self.schedule.report.template)

    def get_docx_report_filename(self):
        """Generate filename based on docx template name and current time."""
        suffix = datetime.now().strftime("%y%m%d%H%M%S")
        filename = Path(str(self.schedule.report.template)).stem
        return f'{filename}_{suffix}.docx'

    def _get_docx_report_output_file(self):
        """Generate filepath."""
        return settings.MEDIA_ROOT / 'tmp' / self.get_docx_report_filename()

    def render_docx_report(self):
        """Renders docx report."""
        template = self._get_docx_report_template()
        output_file = self._get_docx_report_output_file()
        context = self._get_context_for_docx_report()
        docx_template = DocxTemplate(template)
        docx_template.render(context=context)
        docx_template.save(output_file)
        return output_file


class TxtWeekScheduleGenerator:
    """Generate txt report with week schedule."""

    WEEK_DAY_NAMES = {
        '1': 'Понедельник',
        '2': 'Вторник',
        '3': 'Среда',
        '4': 'Четверг',
        '5': 'Пятница',
        '6': 'Суббота',
        '7': 'Воскресенье',
    }

    def __init__(self, week_number):
        self.week_schedule = Schedule.objects.filter(
            date_sheduled__week=week_number
        ).order_by('date_sheduled')

    def _convert_queryset_to_dictionary(self):
        """Converts queryset to defaultdict of defaultdicts"""
        result = defaultdict(lambda: defaultdict(list))
        for shedule in self.week_schedule:
            weekday = shedule.date_sheduled.strftime('%w')
            facility = shedule.equipment_type.facility.facility_name
            equipment = shedule.equipment_type.eqipment_type_name
            to_type = shedule.maintenance_type.m_type
            result[weekday][facility].append({
                'equipment': equipment,
                'to_type': to_type
            })
        return result

    def generate_report(self):
        """Generates week report in txt format."""
        schedule_dict = self._convert_queryset_to_dictionary()
        tmp_text_file = settings.MEDIA_ROOT / 'tmp' / 'txt_report.txt'
        with open(tmp_text_file, 'w') as f:
            for day in schedule_dict:
                f.write(f'{self.WEEK_DAY_NAMES[day]}:\n')
                for facility in schedule_dict[day]:
                    f.write(f'\t{facility}\n')
                    for schedule in schedule_dict[day][facility]:
                        f.write(f'\t\t{schedule["equipment"]} - '
                                f'{schedule["to_type"]}\n')
                f.write('--\n')
