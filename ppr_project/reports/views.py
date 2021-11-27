from datetime import date
from django.views.generic import ListView, View
from django.shortcuts import redirect

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


class MonthScheduleView(ListView):
    model = Schedule
    template_name = 'reports/schedule_month.html'
    context_object_name = 'schedule_plan'
    form_class = ScheduleForm

    def get_queryset(self):
        current_month = 11  # TODO
        return Schedule.objects.filter(date_sheduled__month=current_month)


class DayScheduleView(ListView):
    model = Schedule
    template_name = 'reports/schedule_day.html'
    context_object_name = 'schedule_plan'

    def get_queryset(self):
        today_date = date.today()  # TODO
        return Schedule.objects.filter(date_sheduled=today_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ScheduleForm()
        return context


class ApplyActionToSelectedSchedules(View):

    # TODO  добавить валидацию:
    # если не заполнены журналы - нельзя выполнить работу!!

    def post(self, request):
        selected_action = request.POST.get('selected_action')
        selected_schedules = request.POST.getlist('selected_schedule')
        qs = Schedule.objects.filter(pk__in=selected_schedules)
        if selected_action == '1':
            qs.update(access_journal_filled=True)
        if selected_action == '2':
            qs.update(result_journal_filled=True)
        if selected_action == '3':
            employee1_name = request.POST.get('employee1')
            employee2_name = request.POST.get('employee2')
            employee3_name = request.POST.get('employee3')
            qs.update(
                date_completed=date.today(),
                employee1=employee1_name,
                employee2=employee2_name,
                employee3=employee3_name
            )
        if selected_action == '4':
            # FIXME: Удалить исполнителей
            qs.update(date_completed=None)
        return redirect('reports:day_schedule')

# TODO: подробная информация о каждой работе
