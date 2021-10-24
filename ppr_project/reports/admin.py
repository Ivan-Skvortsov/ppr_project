from django.contrib import admin

from .models import (Employee, Equipment, EquipmentType, Facility,
                     MaintenanceCategory, Schedule, EquipmentMaintenanceRegulation)


admin.site.register(Employee)
admin.site.register(Equipment)
admin.site.register(EquipmentType)
admin.site.register(Facility)
admin.site.register(MaintenanceCategory)
admin.site.register(Schedule)
admin.site.register(EquipmentMaintenanceRegulation)
