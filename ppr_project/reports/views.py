import logging
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import CreateView, FormView, UpdateView

from openpyxl.writer.excel import save_virtual_workbook
from simple_history.utils import bulk_update_with_history

from reports.forms import (CompleteScheduleForm, DateInputForm, DatePeriodForm,
                           ReportDownloadForm, ScheduleCreateForm,
                           ScheduleForm, ScheduleSearchForm,
                           UncompleteReasonForm)
from reports.models import MaintenanceCategory, Schedule
from reports.services import (XlsxReportGenerator,
                              distribute_next_month_works_by_dates,
                              download_photo_approvals, get_next_month_plans)

logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, RedirectView):
    """Redirect to today's schedules."""

    def get_redirect_url(self, *args, **kwargs):
        today = date.today()
        return reverse_lazy('reports:date_range', kwargs={'start_date': today, 'end_date': today})


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'reports/schedule_list.html'
    context_object_name = 'schedule_plan'

    SCHEDULE_ACTION_URLS = {
        'date_scheduled_changed': 'reports:confirm_date_changed',
        'schedule_completed': 'reports:confirm_schedule_completed',
        'schedule_cant_be_completed': 'reports:confirm_schedule_cant_complete'
    }

    def get(self, request, *args, **kwargs):
        request.session['return_url'] = self.request.get_full_path_info()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        selected_schedules = request.POST.getlist('selected_schedule')
        if not selected_schedules:
            messages.warning(self.request, 'Не выбрано ни одной работы!')
            return self.get(request, *args, **kwargs)
        selected_action = request.POST.get('selected_action')
        action_confirmation_url = self.SCHEDULE_ACTION_URLS.get(selected_action)
        if not action_confirmation_url:
            return self.get(request, *args, **kwargs)
        request.session['selected_schedules'] = selected_schedules
        return redirect(action_confirmation_url)

    def get_queryset(self):
        qs = (Schedule.objects.select_related('equipment_type__facility', 'report', 'maintenance_type')
                              .order_by('date_sheduled', 'equipment_type__facility'))
        category = self.request.GET.get('category', None)
        if category:
            maintenance_category = get_object_or_404(MaintenanceCategory, category_name=category)
            return qs.filter(equipment_type__maintenance_category=maintenance_category)
        return qs


class DateRangeScheduleView(ScheduleListView):
    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        date_format = '%Y-%m-%d'
        try:
            start_date_str = self.kwargs.get('start_date')
            self.start_date = datetime.strptime(start_date_str, date_format)
            end_date_str = self.kwargs.get('end_date')
            self.end_date = datetime.strptime(end_date_str, date_format)
            return qs.filter(date_sheduled__range=[self.start_date, self.end_date])
        except ValueError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_format = '%d.%m.%Y'
        start_date = datetime.strftime(self.start_date, date_format)
        end_date = datetime.strftime(self.end_date, date_format)
        context['plan_period'] = f'План на период с {start_date} по {end_date}'
        return context


class SelectDateRangeForScheduleView(LoginRequiredMixin, FormView):
    form_class = DatePeriodForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            date_from = form.data.get('date_from')
            date_to = form.data.get('date_to')
            return redirect('reports:date_range', date_from, date_to)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_to_confirm'] = 'Выберите период'
        context['return_url'] = self.request.session.get('return_url')
        return context


class ScheduleDetailInfoView(LoginRequiredMixin, UpdateView):
    template_name = 'reports/schedule_detail.html'
    model = Schedule
    form_class = ScheduleForm
    context_object_name = 'schedule_entry'

    def get_success_url(self):
        return self.request.session.get('return_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.get_success_url()
        return context


class OverDueScheduleView(ScheduleListView):
    def get_queryset(self):
        qs = super().get_queryset()
        lte_date = date.today() - timedelta(days=1)
        return qs.filter(date_sheduled__lte=lte_date, uncompleted__isnull=True, date_completed__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'Просроченные работы'
        return context


class UncompletableScheduleView(ScheduleListView):
    """View uncompletable schedules for last three months."""

    def get_queryset(self):
        qs = super().get_queryset()
        date_gte = date.today() - timedelta(days=60)
        return qs.filter(
            uncompleted__reason__icontains='магистраль',
            date_completed__isnull=True,
            date_sheduled__gte=date_gte,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'Невыполнимые работы (последние три месяца)'
        return context


class NoPhotoScheduleView(ScheduleListView):
    """View completed schedules without photo approvals."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(date_completed__isnull=False, photo='', maintenance_type__m_type__icontains='Проверка')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'Завершенные проверки защит, к которым не загружены фото'
        return context


class ConfirmScheduleCompletedView(LoginRequiredMixin, FormView):
    form_class = CompleteScheduleForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        schedule_list = self.request.session.get('selected_schedules')
        return_url = self.request.session.get('return_url')
        form = self.get_form(self.form_class)
        if form.is_valid():
            qs = Schedule.objects.filter(pk__in=schedule_list)
            for entry in qs:
                entry._change_reason = 'Confirmed work completed'
                entry.date_completed = form.cleaned_data.get('date_completed')
                entry.employee1 = form.cleaned_data.get('employee1')
                entry.employee2 = form.cleaned_data.get('employee2')
                entry.employee3 = form.cleaned_data.get('employee3')
                entry.uncompleted = None
            bulk_update_with_history(
                qs, Schedule, ['date_completed', 'employee1', 'employee2', 'employee3'], batch_size=500)
            return redirect(return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.request.session.get('return_url')
        context['action_to_confirm'] = 'Выберите дату и исполнителей'
        return context


class ConfirmScheduleDateChangedView(LoginRequiredMixin, FormView):
    form_class = DateInputForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        schedule_list = self.request.session.get('selected_schedules')
        return_url = self.request.session.get('return_url')
        form = self.get_form(self.form_class)
        if form.is_valid():
            qs = Schedule.objects.filter(pk__in=schedule_list)
            for entry in qs:
                entry._change_reason = 'Changed schedule date'
                entry.date_sheduled = form.cleaned_data.get('input_date')
            bulk_update_with_history(qs, Schedule, ['date_sheduled'], batch_size=500)
            return redirect(return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.request.session.get('return_url')
        context['action_to_confirm'] = 'Выберите дату'
        return context


class ConfirmScheduleCannotBeComplete(LoginRequiredMixin, FormView):
    form_class = UncompleteReasonForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        schedule_list = self.request.session.get('selected_schedules')
        return_url = self.request.session.get('return_url')
        form = self.get_form(self.form_class)
        if form.is_valid():
            qs = Schedule.objects.filter(pk__in=schedule_list)
            for entry in qs:
                entry._change_reason = 'Marked as can not be completed'
                entry.uncompleted = form.cleaned_data.get('reason')
            bulk_update_with_history(qs, Schedule, ['uncompleted'], batch_size=500)
            return redirect(return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.request.session.get('return_url')
        context['action_to_confirm'] = 'Выберите дату'
        return context


class SearchView(ScheduleListView):
    template_name = 'reports/schedule_search.html'

    def get_queryset(self):
        filter_params = {k: v for k, v in self.request.GET.items() if v}
        if filter_params:
            qs = super().get_queryset()
            try:
                return qs.filter(**filter_params)
            except Exception as e:
                logger.error(f'Wrong filter params! Error: {e}')
                raise Http404
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ScheduleSearchForm(self.request.GET)
        return context


class XlsxReportDownloadView(LoginRequiredMixin, FormView):
    form_class = ReportDownloadForm
    template_name = 'reports/modal_form_download.html'

    def post(self, request, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            date_from = form.data.get('date_from')
            date_to = form.data.get('date_to')
            report_type = form.data.get('report_type')
            try:
                report_generator = XlsxReportGenerator(date_from, date_to, report_type)
                report = report_generator.render_report()
                response = HttpResponse(
                    content=save_virtual_workbook(report),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
                response['Content-Disposition'] = 'attachment; filename=protocol.xlsx'
                return response
            except Exception as e:
                messages.error(self.request, 'Произошла ошибка! Обратитесь к администратору.', extra_tags='danger')
                logger.error(f'Error rendering xlsx: {e}')
                raise Http404
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_url'] = reverse_lazy('reports:xlsx_report')
        context['modal_window_title'] = 'Выберите тип протокола и период'
        return context


class DistributeNextMonthSchedules(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        try:
            distribute_next_month_works_by_dates()
            messages.success(self.request, 'Распределение работ по дням выполнено!')
        except Exception as e:
            logger.error(f'Error when trying to distribute next month schedules: {e}')
            messages.error(self.request, 'Произошла ошибка при попытке распределения работ!', extra_tags='danger')
        return redirect(self.request.session.get('return_url'))


class XlsxNextMonthDownloadView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        try:
            xlsx_file = get_next_month_plans()
            response = HttpResponse(
                content=save_virtual_workbook(xlsx_file),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = 'attachment; filename=next_month.xlsx'
            return response
        except Exception as e:
            messages.error(self.request, 'Произошла ошибка! Обратитесь к администратору.', extra_tags='danger')
            logger.error(f'Error creating zip file with photos: {e}')
            return redirect(self.request.session.get('return_url'))


class PhotoApprovalsDownloadView(LoginRequiredMixin, FormView):
    form_class = DatePeriodForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            date_from = form.data.get('date_from')
            date_to = form.data.get('date_to')
            try:
                zip_file_path = download_photo_approvals(date_from, date_to)
                return FileResponse(open(zip_file_path, 'rb'))
            except Exception as e:
                messages.error(self.request, 'Произошла ошибка! Обратитесь к администратору.', extra_tags='danger')
                logger.error(f'Error creating zip file with photos: {e}')
                return redirect(self.request.session.get('return_url'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_to_confirm'] = 'Выберите период для скачивания фото'
        context['return_url'] = self.request.session.get('return_url')
        return context


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    form_class = ScheduleCreateForm
    model = Schedule
    template_name = 'reports/action_confirmation.html'

    def get_success_url(self):
        return self.request.session.get('return_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_to_confirm'] = 'Добавить внеплановую работу'
        context['return_url'] = self.get_success_url()
        return context
