from datetime import datetime

from openpyxl import Workbook, worksheet
from openpyxl.styles import Font, Alignment, Border, Side

from django.db.models import Q
from django.template.defaultfilters import date as _date

from reports.models import Schedule


class XlsxReportGenerator:

    def __init__(self, date_from, date_to, report_type):
        self.date_from = date_from
        self.date_to = date_to
        self.report_type = report_type

    def _get_querysets(self) -> tuple:
        qs_filter = {
            'ppr': Q(maintenance_type__m_type__icontains='ТО'),
            'ppz': Q(maintenance_type__m_type__icontains='Проверка'),
            'asps': Q(equipment_type__eqipment_type_name__icontains='АСПС')
        }
        works_list_qs = Schedule.objects.filter(
            date_sheduled__gte=self.date_from,
            date_sheduled__lte=self.date_to,
            date_completed__isnull=False
            ).order_by('date_completed', 'equipment_type__facility')
        return works_list_qs.filter(qs_filter[self.report_type])

    def _render_report_header(self, ws: worksheet, maintenance_type: str):
        date_from = datetime.strptime(self.date_from, '%Y-%m-%d')
        date_to = datetime.strptime(self.date_to, '%Y-%m-%d')
        ws['G1'] = 'Утверждаю'
        ws['A7'] = f'Протокол проведения {maintenance_type}'
        ws['A8'] = 'объектов КС-45 Усинская'
        ws['A9'] = (f'за период с {_date(date_from, "d E")} по '
                    f'{_date(date_to, "d E Y")} г.')
        ws['A11'] = ('Основание проведения работ: График проведения ППР '
                     'оборудования АСУ, А и ТМ КС-45 Усинская на 2022 год.')
        ws['A12'] = ''
        ws.append(['№ п/п',
                   'Объект',
                   'Наименование объекта/системы',
                   'Тип ТО',
                   'Результат',
                   'Дата',
                   'Ответственные лица'])

    def _render_employees_string(self, entry) -> str:
        employees = [
            f'{e.position}\n{e.name}\n\n' for e in (
                entry.employee1, entry.employee2, entry.employee3
            )
            if e is not None and e.position != 'Приборист'
        ]
        return ''.join(employees)

    def _render_report_body(self, ws: worksheet, queryset):
        if queryset.count() == 0:
            ws.append(
                ['', '', 'За выбранный период завершенных работ не найдено']
            )
            return
        for i, work in enumerate(queryset):
            employees = self._render_employees_string(work)
            date_completed = _date(work.date_completed, 'd.m.Y')
            ws.append(
                [i + 1,
                 work.equipment_type.facility.facility_name,
                 work.equipment_type.eqipment_type_name,
                 work.maintenance_type.m_type,
                 'Выполнено.\nЗамечаний нет.',
                 date_completed,
                 employees]
            )
        self._post_process_report(14, ws)

    def _post_process_report(self, start_row: int, ws: worksheet) -> None:
        """Merge cells with same data in cols 2, 6, 7 (Объект, Дата, ФИО)."""
        start_row = start_row
        end_row = ws.max_row
        facility = None
        employees = None
        merge_count = 0
        row_iterator = ws.iter_rows(min_row=start_row, max_row=end_row)
        for row, cells in enumerate(row_iterator, start=start_row):
            if cells[1].value == facility and cells[6].value == employees:
                merge_count += 1
            else:
                if merge_count > 0:
                    ws.merge_cells(start_column=2, end_column=2, start_row=row - merge_count - 1, end_row=row - 1)  # noqa
                    ws.merge_cells(start_column=6, end_column=6, start_row=row - merge_count - 1, end_row=row - 1)  # noqa
                    ws.merge_cells(start_column=7, end_column=7, start_row=row - merge_count - 1, end_row=row - 1)  # noqa
                facility = cells[1].value
                employees = cells[6].value
                merge_count = 0
        if merge_count > 0:
            ws.merge_cells(start_column=2, end_column=2, start_row=row - merge_count, end_row=row)  # noqa
            ws.merge_cells(start_column=6, end_column=6, start_row=row - merge_count, end_row=row)  # noqa
            ws.merge_cells(start_column=7, end_column=7, start_row=row - merge_count, end_row=row)  # noqa

    def _style_worksheet(self, ws: worksheet):
        bold_font = Font(name='Times New Roman', size=12, bold=True)
        regular_font = Font(name='Times New Roman', size=12)

        alignment_center = Alignment(horizontal='center',
                                     vertical='center',
                                     wrap_text=True)
        alignment_top_center = Alignment(horizontal='center',
                                         vertical='top',
                                         wrap_text=True)
        alignment_top_left = Alignment(horizontal='left',
                                       vertical='top',
                                       wrap_text=True)
        border_all = Border(bottom=Side(border_style='thin', color='FF000000'),
                            top=Side(border_style='thin', color='FF000000'),
                            left=Side(border_style='thin', color='FF000000'),
                            right=Side(border_style='thin', color='FF000000'))
        border_bottom = Border(
            bottom=Side(border_style='thin', color='FF000000')
        )

        # worksheet styling
        ws.column_dimensions['A'].width = 4
        ws.column_dimensions['B'].width = 19
        ws.column_dimensions['C'].width = 33
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 19
        ws.column_dimensions['F'].width = 13
        ws.column_dimensions['G'].width = 26
        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_margins.left = 0.5
        ws.page_margins.right = 0.5
        ws.page_margins.top = 0.5
        ws.page_margins.bottom = 0.5
        ws.page_margins.header = 0
        ws.page_margins.footer = 0

        ws.merge_cells(start_row=7, end_row=7, start_column=1, end_column=7)
        ws.merge_cells(start_row=8, end_row=8, start_column=1, end_column=7)
        ws.merge_cells(start_row=9, end_row=9, start_column=1, end_column=7)
        ws.merge_cells(start_row=11, end_row=11, start_column=1, end_column=7)

        for row in ws.iter_rows(min_row=1, max_row=13):
            for cell in row:
                cell.font = bold_font
                cell.alignment = alignment_center
        for cell in ws[13]:
            cell.border = border_all

        ws['G2'].border = ws['G3'].border = ws['G4'].border = border_bottom
        ws['A11'].alignment = Alignment(horizontal='left')
        ws['A11'].font = regular_font

        for row in ws.iter_rows(min_row=14, max_row=ws.max_row):
            for cell in row:
                cell.font = regular_font
                cell.border = border_all
                if cell.column in [1, 4, 5, 6]:
                    cell.alignment = alignment_top_center
                else:
                    cell.alignment = alignment_top_left

    def _render_asps_report(self, ws: worksheet, queryset):
        """
        Renders asps report. This report is different from default
        reports, thats why render and styling of it are united in this
        single function.
        """
        ws.append(
            ['Дата проверки',
             'Местонахождение системы противопожарной защиты',
             'Вид мероприятия по эксплуатации систем противопожарной защиты',
             'Наличие/отсутствие замечаний',
             'Подтверждающий документ (акт, протокол)',
             'Должность,Ф.И.О проводившего проверку']
        )
        ws.append([1, 2, 3, 4, 5, 6])
        if queryset.count() == 0:
            ws.append(
                ['', '', 'За выбранный период завершенных работ не найдено']
            )
            return
        for work in queryset:
            employees = self._render_employees_string(work)
            date_completed = _date(work.date_completed, 'd.m.Y')
            work_type_and_name = (
                f'{work.maintenance_type.m_type}: '
                f'{work.equipment_type.eqipment_type_name}'
            )
            ws.append(
                [date_completed,
                 work.equipment_type.facility.facility_name,
                 work_type_and_name,
                 'Замечаний нет',
                 f'Запись в журнале от {date_completed}',
                 employees.replace('\n', ' ')]
            )

        # styling
        ws.column_dimensions['A'].width = 14
        ws.column_dimensions['B'].width = 40
        ws.column_dimensions['C'].width = 45
        ws.column_dimensions['D'].width = 27
        ws.column_dimensions['E'].width = 40
        ws.column_dimensions['F'].width = 55

        border_all = Border(bottom=Side(border_style='thin', color='FF000000'),
                            top=Side(border_style='thin', color='FF000000'),
                            left=Side(border_style='thin', color='FF000000'),
                            right=Side(border_style='thin', color='FF000000'))
        alignment_center = Alignment(horizontal='center',
                                     vertical='center',
                                     wrap_text=True)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            for cell in row:
                cell.font = Font(name='Times New Roman', size=12)
                cell.border = border_all
                cell.alignment = alignment_center

    def render_styled_report(self):
        rep_type = {
            'ppr': 'ППР оборудования АСУ, А и ТМ',
            'ppz': 'проверок защит'
        }
        wb = Workbook()
        qs = self._get_querysets()
        del wb['Sheet']
        ws = wb.create_sheet(self.report_type)
        if self.report_type == 'asps':
            self._render_asps_report(ws, qs)
            return wb
        self._render_report_header(ws, rep_type[self.report_type])
        self._render_report_body(ws, qs)
        self._style_worksheet(ws)
        return wb
