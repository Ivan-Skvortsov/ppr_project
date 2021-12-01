from datetime import date
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, FormView, UpdateView
from django.urls.base import reverse_lazy, resolve
from django.shortcuts import redirect

from reports.models import EquipmentType, Schedule
from reports.forms import DateInputForm, EmployeeForm, ScheduleForm


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'reports/schedule_list.html'
    context_object_name = 'schedule_plan'

    def post(self, request, *args, **kwargs):
        selected_schedules = request.POST.getlist('selected_schedule')
        if 'date_scheduled_changed' in request.POST:
            return self._redirect_to_confirmation_page(
                selected_schedules,
                'reports:confirm_date_changed'
                )
        if 'schedule_completed' in request.POST:
            return self._redirect_to_confirmation_page(
                selected_schedules,
                'reports:confirm_schedule_completed'
                )
        qs = Schedule.objects.filter(pk__in=selected_schedules)
        if 'access_journal_filled' in request.POST:
            qs.update(access_journal_filled=True)
        if 'result_journal_filled' in request.POST:
            qs.update(result_journal_filled=True)
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

    def get_success_url(self):
        return reverse_lazy(
            'reports:schedule_detail', kwargs={'pk': self.kwargs['pk']})


class ConfirmScheduleCompletedView(FormView):
    form_class = EmployeeForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, *args, **kwargs):
        selected_schedules = kwargs['schedule_list']
        return self.get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse(f'List: {kwargs["schedule_list"]} - page: {kwargs["return_url"]}')


class ConfirmScheduleDateChangedView(FormView):
    form_class = DateInputForm

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'List: {kwargs["schedule_list"]} - page: {kwargs["return_url"]}')
