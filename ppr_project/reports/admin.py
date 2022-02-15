from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from reports.models import (Employee, EquipmentType, Facility,
                            MaintenanceCategory, ReportTemplate, Schedule,
                            MaintenanceType)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'position')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('maintenance_category', 'facility_name')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        'maintenance_category',
        'facility',
        'eqipment_type_name'
    )


@admin.register(Schedule)
class ScheduleAdmin(SimpleHistoryAdmin):
    list_display = (
        'equipment_type',
        'maintenance_type',
        'date_sheduled',
        'date_completed',
        'employee1',
        'employee2',
        'employee3',
        'report'
    )
    list_filter = ('maintenance_type',)
    history_list_display = (
        'date_sheduled',
        'date_completed',
        'employee1',
        'employee2',
        'employee3',
        'photo'
    )


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'm_type')


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(MaintenanceCategory)
