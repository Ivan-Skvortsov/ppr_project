from django.contrib import admin
from django.contrib.admin.decorators import display

from .models import (Employee, Equipment, EquipmentType, Facility,
                     MaintenanceCategory, Schedule,
                     EquipmentMaintenanceRegulation)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'position')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('get_category', 'get_facility', 'equipment_type',
                    'equipment', 'quantity', 'maintenance_regulation')

    @display(description='Facility', ordering='equipment_type__facility')
    def get_facility(self, obj):
        return obj.equipment_type.facility

    @display(description='Maintenance Category',
             ordering='equipment_type__facility__maintenance_category')
    def get_category(self, obj):
        return obj.equipment_type.facility.maintenance_category


admin.site.register(EquipmentType)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('maintenance_category', 'facility_name')


admin.site.register(MaintenanceCategory)
admin.site.register(Schedule)
admin.site.register(EquipmentMaintenanceRegulation)
