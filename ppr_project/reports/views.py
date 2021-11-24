from django.views.generic import ListView

from reports.models import EquipmentType


class IndexView(ListView):
    template_name = 'reports/index.html'
    model = EquipmentType
    context_object_name = 'equipment_type'
