from django.shortcuts import render

from .models import (Employee, Equipment, EquipmentMaintenanceRegulation, EquipmentType, Facility,
                     MaintenanceCategory, Schedule)


def index(request):
    template = 'reports/index.html'
    maintenance_category = MaintenanceCategory.objects.all()
    facility = Facility.objects.all()
    eqipment_type = EquipmentType.objects.all()
    eqipment = Equipment.objects.all()
    regulations = EquipmentMaintenanceRegulation.objects.all()
    context = {
        'maintenance_category': maintenance_category,
        'facility': facility,
        'eqipment_type': eqipment_type,
        'eqipment': eqipment,
        'regulations': regulations
    }
    return render(request, template, context)
