from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.urls.base import resolve
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView

from reports.forms import DateInputForm, EmployeeForm, ScheduleForm
from reports.models import EquipmentType, MaintenanceCategory, Schedule
from reports.services import DocxReportGenerator


class ScheduleListView(LoginRequiredMixin, ListView):
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

        return self.get(request, *args, **kwargs)

    def _redirect_to_confirmation_page(self, selected_schedules, page_url):
        return_url = resolve(self.request.path_info).url_name
        schedule_list = '_'.join(selected_schedules)
        return redirect(
            page_url,
            schedule_list=schedule_list,
            return_url=return_url
        )


class DayScheduleView(ScheduleListView):

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        if category_id:
            maintenance_category = get_object_or_404(
                MaintenanceCategory,
                pk=category_id
            )
            return Schedule.objects.filter(
                date_sheduled=date.today(),
                equipment_type__maintenance_category=maintenance_category
            )
        return Schedule.objects.filter(date_sheduled=date.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на день'
        context['plan_url'] = reverse_lazy('reports:day_schedule')
        return context


class MonthScheduleView(ScheduleListView):

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        month = date.today().month
        if category_id:
            maintenance_category = get_object_or_404(
                MaintenanceCategory,
                pk=category_id
            )
            return Schedule.objects.filter(
                date_sheduled__month=month,
                equipment_type__maintenance_category=maintenance_category
            )
        return Schedule.objects.filter(date_sheduled__month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на месяц'
        context['plan_url'] = reverse_lazy('reports:month_schedule')
        return context


class WeekScheduleView(ScheduleListView):

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        week = date.today().isocalendar()[1]  # Get week number
        if category_id:
            maintenance_category = get_object_or_404(
                MaintenanceCategory,
                pk=category_id
            )
            return Schedule.objects.filter(
                date_sheduled__week=week,
                equipment_type__maintenance_category=maintenance_category
            )
        return Schedule.objects.filter(date_sheduled__week=week)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на неделю'
        context['plan_url'] = reverse_lazy('reports:week_schedule')
        return context


class YearScheduleView(ScheduleListView):

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        year = date.today().year
        if category_id:
            maintenance_category = get_object_or_404(
                MaintenanceCategory,
                pk=category_id
            )
            return Schedule.objects.filter(
                date_sheduled__year=year,
                equipment_type__maintenance_category=maintenance_category
            )
        return Schedule.objects.filter(date_sheduled__year=year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на год'
        context['plan_url'] = reverse_lazy('reports:year_schedule')
        return context


class IndexView(LoginRequiredMixin, ListView):

    #  ВРЕМЕННАЯ ЗАГЛУШКА
    def get(self, request, *args, **kwargs):
        return redirect('reports:week_schedule')

    template_name = 'reports/index.html'
    model = EquipmentType
    context_object_name = 'equipment_type'

    def get_queryset(self):
        return super().get_queryset()


class ScheduleDetailInfoView(LoginRequiredMixin, UpdateView):
    template_name = 'reports/schedule_detail.html'
    model = Schedule
    form_class = ScheduleForm
    context_object_name = 'schedule_entry'

    def get_success_url(self):
        return_url = f'reports:{self.kwargs["return_url"]}'
        return reverse_lazy(return_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = f'reports:{self.kwargs["return_url"]}'
        context['return_url'] = reverse_lazy(return_url)
        return context


class ConfirmScheduleCompletedView(LoginRequiredMixin, FormView):
    form_class = EmployeeForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = f'reports:{kwargs["return_url"]}'
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            qs.update(
                date_completed=date.today(),
                employee1=self.form.cleaned_data['employee1'],
                employee2=self.form.cleaned_data['employee2'],
                employee3=self.form.cleaned_data['employee3']
            )
            return redirect(self.return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = f'reports:{self.kwargs["return_url"]}'
        context['return_url'] = reverse_lazy(return_url)
        context['action_to_confirm'] = 'Выберите исполнителей работ'
        return context


class ConfirmScheduleDateChangedView(LoginRequiredMixin, FormView):
    form_class = DateInputForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = f'reports:{kwargs["return_url"]}'
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            qs.update(date_sheduled=self.form.cleaned_data['input_date'])
            return redirect(self.return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = f'reports:{self.kwargs["return_url"]}'
        context['return_url'] = reverse_lazy(return_url)
        context['action_to_confirm'] = 'Выберите дату'
        return context


class DocxReportDownloadView(View):

    def get(self, request, schedule_id):

        try:
            report_generator = DocxReportGenerator(schedule_id)
            docx_file = report_generator.render_docx_report()
            docx_filename = report_generator.get_docx_report_filename()
            with open(docx_file, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # noqa: E501
                )
            response['Content-Disposition'] = 'inline; filename=' + docx_filename  # noqa: E501
            return response
        except Exception as e:
            print(f'Error rendering docx: {e}')  # FIXME: logging!
            raise Http404
