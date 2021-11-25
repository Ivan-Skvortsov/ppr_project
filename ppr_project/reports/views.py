from django.views.generic import ListView

from reports.models import EquipmentType, Schedule


class IndexView(ListView):
    template_name = 'reports/index.html'
    model = EquipmentType
    context_object_name = 'equipment_type'

    def get_queryset(self):
        return super().get_queryset()


class YearScheduleView(ListView):
    template_name = 'reports/schedule_year.html'
    model = Schedule
    context_object_name = 'schedule_plan'


class MonthScheduleView(ListView):
    template_name = 'reports/schedule_year.html'
    model = Schedule
    context_object_name = 'schedule_plan'

    def get_queryset(self):
        return Schedule.objects.filter(date_sheduled__month=12)
