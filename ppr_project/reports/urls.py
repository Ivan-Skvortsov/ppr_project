from django.urls import path

from reports.views import (ConfirmScheduleCompletedView,
                           ConfirmScheduleDateChangedView, DayScheduleView,
                           DocxReportDownloadView, IndexView,
                           MonthScheduleView, ScheduleDetailInfoView,
                           WeekScheduleView, YearScheduleView, OverDueScheduleView,
                           SearchView)

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('year/<int:category_id>/', YearScheduleView.as_view(), name='year_schedule'),  # noqa: E501
    path('year/', YearScheduleView.as_view(), name='year_schedule'),
    path('month/<int:category_id>/', MonthScheduleView.as_view(), name='month_schedule'),  # noqa: E501
    path('month/', MonthScheduleView.as_view(), name='month_schedule'),
    path('week/<int:category_id>/', WeekScheduleView.as_view(), name='week_schedule'),  # noqa: E501
    path('week/', WeekScheduleView.as_view(), name='week_schedule'),
    path('day/<int:category_id>/', DayScheduleView.as_view(), name='day_schedule'),  # noqa: E501
    path('day/', DayScheduleView.as_view(), name='day_schedule'),
    path('overdue/<int:category_id>/', OverDueScheduleView.as_view(), name='overdue'),  # noqa: E501
    path('overdue/', OverDueScheduleView.as_view(), name='overdue'),
    path('search/', SearchView.as_view(), name='search'),


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
