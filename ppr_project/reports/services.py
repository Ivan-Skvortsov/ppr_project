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
            'remarks': None,  # FIXME: add remarks to schedule model
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
        """Remders docx report."""
        template = self._get_docx_report_template()
        output_file = self._get_docx_report_output_file()
        context = self._get_context_for_docx_report()
        docx_template = DocxTemplate(template)
        docx_template.render(context=context)
        docx_template.save(output_file)
        return output_file


class TxtWeekScheduleGenerator:
    """Generate txt report with next week schedule."""  # TODO

    def __init__(self, week_number):
        self.week_schedule = Schedule.objects.filter(
            date_sheduled__week=week_number
        ).order_by('date_sheduled')

    def generate_report(self):
        out = defaultdict(list)
        for shedule in self.week_schedule:
            weekday = shedule.date_sheduled.strftime('%w')
            out[weekday].append({
                'facility': shedule.equipment_type.facility,
                'equipment': shedule.equipment_type,
                'to_type': shedule.maintenance_type
            })
        return out




"""
Понедельник:
--
Общее по всем объектам КЦ-1
	Датчики T, осмотр кабельной продукции - ТО-4
	Датчики P, осмотр кабельной продукции - ТО-2
ГПА-12
 	АСКЗ - проверка
	АСПС, ПТ - проверка
Котельная НК-Терм
	Датчики L - ТО-3

Вторник
--
	
"""