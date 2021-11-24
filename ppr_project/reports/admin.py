from django.contrib import admin

from reports.models import (Employee, EquipmentType, Facility,
                            MaintenanceCategory, Schedule)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'position')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('maintenance_category', 'facility_name')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('maintenance_category',
                    'facility',
                    'eqipment_type_name',
                    'report_template')


admin.site.register(MaintenanceCategory)
admin.site.register(Schedule)
