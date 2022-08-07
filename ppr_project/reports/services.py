from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, NamedStyle

from django.template.defaultfilters import date as _date

from reports.models import Schedule


class XlsxReportGenerator:

    def __init__(self, type, period):
        self.type = type
        self.period = period
        week = date.today().isocalendar()[1]
        self.qs = Schedule.objects.filter(
            maintenance_type__m_type__icontains='ТО',
            date_sheduled__week=week,
            date_completed__isnull=False
            ).order_by('date_completed', 'equipment_type__facility')

    def _render_report_header(self):
        wb = Workbook()
        ws = wb.active
        ws['G1'] = 'Утверждаю'
        ws['A7'] = 'Протокол проведения ППР оборудования АСУ, А и ТМ'
        ws['A8'] = 'объектов КС-45 Усинская'
        ws['A9'] = _date(self.qs[0].date_sheduled, 'F Y')
        ws['A11'] = ('Основание проведения работ: График проведения ППР '
                     'оборудования АСУ, А и ТМ КС-45 Усинская на 2022 год.')
        ws['A12'] = ''
        ws.append(['№ п/п',
                   'Объект',
                   'Наименование объекта/системы',
                   'Тип ТО',
                   'Результат ТО',
                   'Дата',
                   'Ответственные лица'])
        return wb

    def _render_report_body(self, report: Workbook) -> Workbook:
        ws = report.active
        for i, work in enumerate(self.qs):
            employees = (
                f'{work.employee1.position}\n{work.employee1.name}\n'
                f'{work.employee2.position}\n{work.employee2.name}\n'
            )
            if work.employee3 is not None:
                employees += (
                    f'{work.employee3.position}\n{work.employee3.name}\n'
                )
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
        self._post_process_report(14, report)
        return report

    def _post_process_report(self, start_row: int, report: Workbook) -> None:
        """Merge cells with same data in cols 2, 6, 7 (Объект, Дата, ФИО)."""
        ws = report.active
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

    def _style_report(self, report: Workbook):
        ws = report.active
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
        ws.column_dimensions['D'].width = 9
        ws.column_dimensions['E'].width = 19
        ws.column_dimensions['F'].width = 13
        ws.column_dimensions['G'].width = 27
        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_margins.left = 0.5
        ws.page_margins.right = 0.5
        ws.page_margins.top = 0.5
        ws.page_margins.bottom = 0.5
        ws.page_margins.header = 0
        ws.page_margins.footer = 0

        # header styling
        header_style = NamedStyle(name='header_style')
        header_style.font = bold_font
        header_style.alignment = alignment_center

        ws.merge_cells(start_row=7, end_row=7, start_column=1, end_column=7)
        ws.merge_cells(start_row=8, end_row=8, start_column=1, end_column=7)
        ws.merge_cells(start_row=9, end_row=9, start_column=1, end_column=7)
        ws.merge_cells(start_row=11, end_row=11, start_column=1, end_column=7)

        for row in ws.iter_rows(min_row=1, max_row=13):
            for cell in row:
                cell.style = header_style
        for cell in ws[13]:
            cell.border = border_all

        ws['G2'].border = ws['G3'].border = ws['G4'].border = border_bottom
        ws['A11'].alignment = Alignment(horizontal='left')
        ws['A11'].font = regular_font

        # body styling
        body_style = NamedStyle(name='body_style')
        body_style.font = regular_font
        body_style.border = border_all
        body_style.alignment = alignment_top_left

        for row in ws.iter_rows(min_row=14, max_row=ws.max_row):
            for cell in row:
                cell.style = body_style
                if cell.column in [1, 4, 5, 6]:
                    cell.alignment = alignment_top_center
        return report

    def render_report(self):
        header = self._render_report_header()
        return self._render_report_body(header)

    def render_styled_report(self):
        report = self.render_report()
        return self._style_report(report)
