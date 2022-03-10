from datetime import date

from openpyxl import load_workbook
from reports.models import (EquipmentType, Facility, MaintenanceCategory,
                            MaintenanceType, Schedule, ReportTemplate)
from tqdm import tqdm


def import_objects_from_xls(filename, category_name):
    """Imports objects from xlsx file."""
    category = MaintenanceCategory.objects.get_or_create(
        category_name=category_name)[0]
    wb = load_workbook(filename=filename, read_only=True, data_only=True)
    worksheet = wb.active
    for row in tqdm(worksheet.iter_rows(min_row=2), total=100):
        facility_name = row[0].value
        if not facility_name:
            return
        eqipment_type_name = row[1].value

        facility = Facility.objects.get_or_create(
            facility_name=facility_name,
            maintenance_category=category
        )[0]

        EquipmentType.objects.create(
            facility=facility,
            eqipment_type_name=eqipment_type_name,
            maintenance_category=category
        )


def import_schedule_from_xls(filename, category_name):
    """Import schedules from xlsx file."""
    wb = load_workbook(filename=filename, read_only=True, data_only=True)
    worksheet = wb.active
    for row in tqdm(worksheet.iter_rows(min_row=2), total=100):
        category = MaintenanceCategory.objects.get(category_name=category_name)
        facility_name = row[0].value
        if not facility_name:
            return
        facility = Facility.objects.get(
            facility_name=facility_name,
            maintenance_category=category
        )
        equipment_type = EquipmentType.objects.get(
            facility=facility,
            maintenance_category=category,
            eqipment_type_name=row[1].value
        )
        for i in range(2, 14):
            if row[i].value:
                m_type = MaintenanceType.objects.get_or_create(
                    m_type=row[i].value.strip()
                )[0]
                date_scheduled = date(2022, i-1, 1)
                Schedule.objects.create(
                    equipment_type=equipment_type,
                    maintenance_type=m_type,
                    date_sheduled=date_scheduled
                )


def execute_import_schedules_and_objects(filename):
    category_name = input('Введите категорию: ')
    print('Creating objects: \n')
    import_objects_from_xls(filename, category_name)
    print('Creating schedules: \n')
    import_schedule_from_xls(filename, category_name)
    print('Finished!')


def import_templates_from_xls(filename):
    """Import templates from xlsx file."""
    wb = load_workbook(filename=filename, read_only=True, data_only=True)
    worksheet = wb.active
    for row in worksheet.iter_rows(min_row=2):
        for cell in (row[14], row[15], row[16], row[17]):
            if cell.value:
                report_name = cell.value
                template_path = 'templates/' + cell.value + '.docx'
                ReportTemplate.objects.get_or_create(
                    template_name=report_name,
                    template=template_path
                )


def update_template_in_schedules(filename):
    """Updates field `report` in schedule model instances."""
    maintenance_types = {
        14: 'ТО',
        15: 'ТО-3',
        16: 'ТО-4',
        17: 'Проверка'
    }
    wb = load_workbook(filename=filename, read_only=True, data_only=True)
    worksheet = wb.active
    for row in worksheet.iter_rows(min_row=2):
        for column_number in maintenance_types:
            if row[column_number].value:
                print(row[column_number].value)
                template = ReportTemplate.objects.get(
                    template_name=row[column_number].value
                )
                equipment_type = EquipmentType.objects.get(
                    facility__facility_name=row[0].value,
                    eqipment_type_name=row[1].value
                    )
                qs = Schedule.objects.filter(
                    equipment_type=equipment_type,
                    maintenance_type__m_type=maintenance_types[column_number]
                )
                qs.update(report=template)


def execute_import_templates(filename):
    print('Importing templates...')
    import_templates_from_xls(filename)
    print('Updating schedules...')
    update_template_in_schedules(filename)
