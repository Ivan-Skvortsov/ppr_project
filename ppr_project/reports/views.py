from django.views.generic import ListView

from reports.models import EquipmentType, Schedule


class IndexView(ListView):
    template_name = 'reports/index.html'
    model = EquipmentType
    context_object_name = 'equipment_type'


class YearScheduleView(ListView):
    template_name = 'reports/schedule_year.html'
    model = Schedule
    context_object_name = 'year_plan'
