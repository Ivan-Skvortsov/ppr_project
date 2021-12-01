from datetime import date
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, FormView, UpdateView
from django.urls.base import reverse_lazy

from reports.models import EquipmentType, Schedule
from reports.forms import DateInputForm, EmployeeForm, ScheduleForm


class ScheduleListView(ListView, FormMixin):
    model = Schedule
    form_class = DateInputForm
    form_class_employees = EmployeeForm
    template_name = 'reports/schedule_list.html'
    context_object_name = 'schedule_plan'

    def get(self, request, *args, **kwargs):
        self.date_input_form = self.get_form(self.form_class)
        self.employees_form = self.get_form(self.form_class_employees)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        selected_schedules = request.POST.getlist('selected_schedule')
        qs = Schedule.objects.filter(pk__in=selected_schedules)

        if 'access_journal_filled' in request.POST:
            qs.update(access_journal_filled=True)

        if 'result_journal_filled' in request.POST:
            qs.update(result_journal_filled=True)

        if 'date_scheduled_changed' in request.POST:
            self.date_input_form = self.get_form(self.form_class)
            if self.date_input_form.is_valid():
                date_scheduled = self.date_input_form.cleaned_data[
                    'input_date'
                ]
                qs.update(date_sheduled=date_scheduled)

        if 'schedule_completed' in request.POST:
            self.employees_form = self.get_form(self.form_class_employees)
            self.employees_form = EmployeeForm(request.POST)
            if self.employees_form.is_valid():
                employee1 = self.employees_form.cleaned_data['employee1']
                employee2 = self.employees_form.cleaned_data['employee2']
                employee3 = self.employees_form.cleaned_data['employee3']
                qs.update(
                    date_completed=date.today(),
                    employee1=employee1,
                    employee2=employee2,
                    employee3=employee3,
                )

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ScheduleListView, self).get_context_data(
            *args, **kwargs
        )
        context['date_input_form'] = self.date_input_form
        context['employees_form'] = self.employees_form
        return context


class DayScheduleView(ScheduleListView):

    def get_queryset(self):
        return Schedule.objects.filter(date_sheduled=date.today())


class MonthScheduleView(ScheduleListView):

    def get_queryset(self):
        month = date.today().month
        return Schedule.objects.filter(date_sheduled__month=month)


class WeekScheduleView(ScheduleListView):

    def get_queryset(self):
        week = date.today().isocalendar()[1]  # Get week number
        print(week)
        return Schedule.objects.filter(date_sheduled__week=week)


class YearScheduleView(ScheduleListView):

    def get_queryset(self):
        year = date.today().year
        return Schedule.objects.filter(date_sheduled__year=year)


class IndexView(ListView):
    template_name = 'reports/index.html'
    model = EquipmentType
    context_object_name = 'equipment_type'

    def get_queryset(self):
        return super().get_queryset()


class ScheduleDetailInfo(UpdateView):
    template_name = 'reports/schedule_detail.html'
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        return reverse_lazy(
            'reports:schedule_detail', kwargs={'pk': self.kwargs['pk']})


class ConfirmScheduleAction(FormView):
    form_class = DateInputForm

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'List: {kwargs["schedule_list"]} - page: {kwargs["return_page"]}')
