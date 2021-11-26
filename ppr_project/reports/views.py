from datetime import date
from django.forms.forms import Form
from django.views.generic import ListView, FormView

from reports.models import EquipmentType, Schedule
from reports.forms import ScheduleForm

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


class MonthScheduleView(FormView):
    model = Schedule
    template_name = 'reports/schedule_month.html'
    context_object_name = 'schedule_plan'
    form_class = ScheduleForm

    def get_queryset(self):
        current_month = 12  #  TODO
        return Schedule.objects.filter(date_sheduled__month=current_month)


class DayScheduleView(ListView):
    model = Schedule
    template_name = 'reports/schedule_day.html'
    context_object_name = 'schedule_plan'

    def get_queryset(self):
        today_date = date.today()  # TODO
        return Schedule.objects.filter(date_scheduled=today_date)
