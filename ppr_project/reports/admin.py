from typing import DefaultDict
from django.contrib import admin

from .models import Employee, Equipment, EquipmentType, Facility, Job


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'position', 'department')
    

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_facility', 'equipment_type', 'equipment', 'quantity')

    def get_facility(self, obj):
        return obj.equipment_type.facility
    get_facility.short_description = 'Facility_FK!'
    get_facility.admin_order_field = 'equipment_type__facility'

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'facility', 'eq_type_name')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'facility_name')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'asu_engineer', 'facility_id', 'equipment_type', 'job_date')
