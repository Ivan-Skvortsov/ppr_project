from django.contrib import admin

from .models import (Employee, Equipment, EquipmentType, Facility,
                     MaintenanceCategory, Schedule)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'position', 'department')


@admin.register(MaintenanceCategory)
class MaintenanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category_name')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'maintenance_category', 'facility_name')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'facility', 'eq_type_name')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_facility',
                    'equipment_type', 'equipment', 'quantity')

    def get_facility(self, obj):
        return obj.equipment_type.facility
    get_facility.short_description = 'Facility_FK!'
    get_facility.admin_order_field = 'equipment_type__facility'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
