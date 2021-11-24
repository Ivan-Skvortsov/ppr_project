from openpyxl import load_workbook


from reports.models import EquipmentType, Facility, MaintenanceCategory


def import_from_xls(filename):
    category_name = 'ППР КЦ-1'
    category = MaintenanceCategory.objects.get(category_name=category_name)
    wb = load_workbook(filename=filename, read_only=True, data_only=True)
    worksheet = wb.active
    for row in worksheet.iter_rows(min_row=2):
        facility_name = row[0].value
        eqipment_type_name = row[1].value

        facility = Facility.objects.get_or_create(
            facility_name=facility_name,
            maintenance_category=category
        )[0]
        print(facility)
        equipment = EquipmentType.objects.create(
            facility=facility,
            eqipment_type_name=eqipment_type_name,
            maintenance_category=category
        )
        print(f'EQ:{equipment}')
    eq_type_count = EquipmentType.objects.count()
    facilities_count = Facility.objects.count()
    return f'Added {facilities_count} facilites and {eq_type_count} eq types.'
