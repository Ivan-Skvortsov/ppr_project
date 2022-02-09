from django.urls import path

from reports.views import (ConfirmScheduleCompletedView,
                           ConfirmScheduleDateChangedView, DayScheduleView,
                           DocxReportDownloadView, IndexView,
                           MonthScheduleView, ScheduleDetailInfoView,
                           WeekScheduleView, YearScheduleView)

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('year/', YearScheduleView.as_view(), name='year_schedule'),
    path('month/', MonthScheduleView.as_view(), name='month_schedule'),
    path('week/', WeekScheduleView.as_view(), name='week_schedule'),
    path('day/', DayScheduleView.as_view(), name='day_schedule'),
    path(
        'schedule/<int:pk>/<str:return_url>/',
        ScheduleDetailInfoView.as_view(),
        name='schedule_detail'
    ),
    path(
        'schedule/confirm_completed/<slug:schedule_list>/<str:return_url>/',
        ConfirmScheduleCompletedView.as_view(),
        name='confirm_schedule_completed'
    ),
    path(
        'schedule/confirm_date_changed/<slug:schedule_list>/<str:return_url>/',
        ConfirmScheduleDateChangedView.as_view(),
        name='confirm_date_changed'
    ),
    path(
        'docx_report/<int:schedule_id>/',
        DocxReportDownloadView.as_view(),
        name='docx_report'
    ),
]
