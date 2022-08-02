import json
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.urls.base import resolve
from django.views import View
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import FormView, UpdateView

from simple_history.utils import bulk_update_with_history

from reports.forms import (DateInputForm, CompleteScheduleForm, ScheduleForm,
                           ScheduleSearchForm, UncompleteReasonForm)
from reports.models import MaintenanceCategory, Schedule
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
        if selected_action == 'schedule_cant_be_completed':
            return self._redirect_to_confirmation_page(
                selected_schedules,
                'reports:confirm_schedule_cant_complete'
                )
        qs = Schedule.objects.filter(pk__in=selected_schedules)
        if selected_action == 'access_journal_filled':
            for entry in qs:
                entry._change_reason = 'Changed state of access journal'
                entry.access_journal_filled = True
            bulk_update_with_history(
                qs, Schedule, ['access_journal_filled'], batch_size=500
            )
        if selected_action == 'result_journal_filled':
            for entry in qs:
                entry._change_reason = 'Changed state of result journal'
                entry.result_journal_filled = True
            bulk_update_with_history(
                qs, Schedule, ['result_journal_filled'], batch_size=500
            )
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        qs = (Schedule.objects.select_related('equipment_type__facility',
                                              'report',
                                              'maintenance_type')
                              .order_by('date_sheduled',
                                        'equipment_type__facility'))
        if category_id:
            maintenance_category = get_object_or_404(
                MaintenanceCategory, pk=category_id
            )
            return qs.filter(
                equipment_type__maintenance_category=maintenance_category
            )
        return qs

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
        qs = super().get_queryset()
        return qs.filter(date_sheduled=date.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на сегодня'
        context['plan_url'] = reverse_lazy('reports:day_schedule')
        return context


class MonthScheduleView(ScheduleListView):

    def get_queryset(self):
        qs = super().get_queryset()
        month = date.today().month
        return qs.filter(date_sheduled__month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на этот месяц'
        context['plan_url'] = reverse_lazy('reports:month_schedule')
        return context


class WeekScheduleView(ScheduleListView):

    def get_queryset(self):
        qs = super().get_queryset()
        week = date.today().isocalendar()[1]  # Get week number
        return qs.filter(date_sheduled__week=week)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на эту неделю'
        context['plan_url'] = reverse_lazy('reports:week_schedule')
        return context


class NextMonthScheduleView(ScheduleListView):

    def get_queryset(self):
        qs = super().get_queryset()
        next_month = date.today().month + 1
        return qs.filter(date_sheduled__month=next_month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'План на следующий месяц'
        context['plan_url'] = reverse_lazy('reports:next_month_schedule')
        return context


class IndexView(LoginRequiredMixin, RedirectView):

    url = reverse_lazy('reports:week_schedule')


class OverDueScheduleView(ScheduleListView):

    def get_queryset(self):
        qs = super().get_queryset()
        lte_date = date.today() - timedelta(days=1)
        return qs.filter(
            date_sheduled__lte=lte_date,
            uncompleted__isnull=True,
            date_completed__isnull=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'Просроченные работы'
        context['plan_url'] = reverse_lazy('reports:overdue')
        return context


class UncompletableScheduleView(ScheduleListView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            uncompleted__isnull=False, date_completed__isnull=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan_period'] = 'Невыполнимые работы'
        context['plan_url'] = reverse_lazy('reports:uncompletable')
        return context


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
    form_class = CompleteScheduleForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = f'reports:{kwargs["return_url"]}'
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            for entry in qs:
                entry._change_reason = 'Confirmed work completed'
                entry.date_completed = self.form.cleaned_data['date_completed']
                entry.employee1 = self.form.cleaned_data['employee1']
                entry.employee2 = self.form.cleaned_data['employee2']
                entry.employee3 = self.form.cleaned_data['employee3']
            bulk_update_with_history(
                qs,
                Schedule,
                ['date_completed', 'employee1', 'employee2', 'employee3'],
                batch_size=500
            )
            return redirect(self.return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = f'reports:{self.kwargs["return_url"]}'
        context['return_url'] = reverse_lazy(return_url)
        context['action_to_confirm'] = 'Выберите дату и исполнителей'
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
            for entry in qs:
                entry._change_reason = 'Changed schedule date'
                entry.date_sheduled = self.form.cleaned_data['input_date']
            bulk_update_with_history(
                qs, Schedule, ['date_sheduled'], batch_size=500
            )
            return redirect(self.return_url)
        return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = f'reports:{self.kwargs["return_url"]}'
        context['return_url'] = reverse_lazy(return_url)
        context['action_to_confirm'] = 'Выберите дату'
        return context


class ConfirmScheduleCannotBeComplete(LoginRequiredMixin, FormView):
    form_class = UncompleteReasonForm
    template_name = 'reports/action_confirmation.html'

    def post(self, request, **kwargs):
        self.schedule_list = kwargs['schedule_list'].split('_')
        self.return_url = f'reports:{kwargs["return_url"]}'
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            qs = Schedule.objects.filter(pk__in=self.schedule_list)
            for entry in qs:
                entry._change_reason = 'Marked as can not be completed'
                entry.uncompleted = self.form.cleaned_data['reason']
            bulk_update_with_history(
                qs, Schedule, ['uncompleted'], batch_size=500
            )
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


class SearchView(ScheduleListView):
    template_name = 'reports/schedule_search.html'

    def get_queryset(self):
        filter_params = {k: v for k, v in self.request.GET.items() if v}
        if filter_params:
            qs = super().get_queryset()
            try:
                return qs.filter(**filter_params)
            except Exception as e:
                print(f'Wrong filter params! Error: {e}')  # FIXME: logging!
                raise Http404
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ScheduleSearchForm(self.request.GET)
        return context


class MarkJournalFilledView(LoginRequiredMixin, View):
    """View for fetch-api calls."""

    def post(self, request, pk):
        if not request.body:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        shedule = get_object_or_404(Schedule, pk=pk)
        data = json.loads(request.body)
        action = data.get('action')
        is_checked = data.get('is_checked')
        if action == 'access_journal_filled':
            shedule.access_journal_filled = is_checked
            shedule._change_reason = 'Changed state of access journal'
        elif action == 'result_journal_filled':
            shedule.result_journal_filled = is_checked
            shedule._change_reason = 'Changed state of result journal'
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        shedule.save()
        completed = all([shedule.access_journal_filled,
                        shedule.result_journal_filled,
                        shedule.date_completed])
        return JsonResponse({'completed': completed})
