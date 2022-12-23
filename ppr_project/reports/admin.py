from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from reports.models import (Employee, EquipmentType, Facility,
                            MaintenanceCategory, MaintenanceType,
                            ReportTemplate, Schedule, UncompleteReasons)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'position')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('maintenance_category', 'facility_name')
    list_filter = ('maintenance_category',)


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
        'get_facility',
        'equipment_type',
        'maintenance_type',
        'date_sheduled',
        'date_completed',
    )
    list_filter = (
        'maintenance_type',
        'date_sheduled',
        'date_completed',
        'equipment_type__facility__maintenance_category'
    )
    search_fields = (
        'equipment_type__eqipment_type_name',
        'equipment_type__facility__facility_name'
    )
    history_list_display = (
        'date_sheduled',
        'date_completed',
        'employee1',
        'employee2',
        'employee3',
        'photo'
    )

    @admin.display
    def get_facility(self, obj):
        return obj.equipment_type.facility.facility_name


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'm_type')


@admin.register(UncompleteReasons)
class UncompleteReasonsAdmin(admin.ModelAdmin):
    pass


@admin.register(MaintenanceCategory)
class MaintenanceCategoryAdmin(admin.ModelAdmin):
    pass
