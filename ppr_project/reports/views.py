from datetime import date
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from django.urls.base import reverse_lazy, resolve
from django.shortcuts import redirect
from django.contrib import messages

from reports.models import EquipmentType, Schedule
from reports.forms import DateInputForm, EmployeeForm, ScheduleForm


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'reports/schedule_list.html'
    context_object_name = 'schedule_plan'

    def post(self, request, *args, **kwargs):
        selected_schedules = request.POST.getlist('selected_schedule')
        selected_action = request.POST['selected_action']
        if not selected_schedules:
            messages.warning(self.request, 'Не выбрано ни одной работы!')
            return self.get(request, *args, **kwargs)
        if selected_action == 'date_scheduled_changed':
            return self._redirect_to_confirmation_page(
                selected_schedules,
                'reports:confirm_date_changed'
                )
        if selected_action == 'schedule_completed':
            return self._redirect_to_confirmation_page(
                selected_schedules,
                'reports:confirm_schedule_completed'
                )
        qs = Schedule.objects.filter(pk__in=selected_schedules)
        if selected_action == 'access_journal_filled':
            qs.update(access_journal_filled=True)
        if selected_action == 'result_journal_filled':
            qs.update(result_journal_filled=True)

        messages.success(self.request, 'Заполнение журнала отмечено!')
        return self.get(request, *args, **kwargs)

    def _redirect_to_confirmation_page(self, selected_schedules, page_url):
        resolved_url = resolve(self.request.path_info)
        current_namespace = resolved_url.namespace
        current_url_name = resolved_url.url_name
        return_url = f'{current_namespace}:{current_url_name}'
        schedule_list = '_'.join(selected_schedules)
        return redirect(
            page_url,
            schedule_list=schedule_list,
            return_url=return_url
        )


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


class ScheduleDetailInfoView(UpdateView):
    template_name = 'reports/schedule_detail.html'
    model = Schedule
    form_class = ScheduleForm
    context_object_name = 'schedule_entry'

    def get_success_url(self):
        return self.request.POST.get('next_page', '/')


class ConfirmScheduleCompletedView(FormView):
    form_class = EmployeeForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = kwargs['return_url']
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            qs.update(
                date_completed=date.today(),
                employee1=self.form.cleaned_data['employee1'],
                employee2=self.form.cleaned_data['employee2'],
                employee3=self.form.cleaned_data['employee3']

            )
            messages.success(self.request, 'Проведение работ отмечено!')
            return redirect(self.return_url)
        return self.get(request, **kwargs)


class ConfirmScheduleDateChangedView(FormView):
    form_class = DateInputForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = kwargs['return_url']
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            qs.update(date_sheduled=self.form.cleaned_data['input_date'])
            messages.success(
                self.request,
                'Плановая дата проведения работ изменена!'
            )
            return redirect(self.return_url)
        return self.get(request, **kwargs)
