from django.urls import path

from reports.views import (
    ConfirmScheduleCannotBeComplete,
    ConfirmScheduleCompletedView,
    ConfirmScheduleDateChangedView,
    DayScheduleView,
    DistributeNextMonthSchedules,
    IndexView,
    MonthScheduleView,
    NextMonthScheduleView,
    NoPhotoScheduleView,
    OverDueScheduleView,
    ScheduleDetailInfoView,
    SearchView,
    UncompletableScheduleView,
    WeekScheduleView,
    XlsxNextMonthDownloadView,
    XlsxReportDownloadView,
)

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(
        'next_month/<int:category_id>/',
        NextMonthScheduleView.as_view(),
        name='next_month_schedule',
    ),
    path('next_month/', NextMonthScheduleView.as_view(), name='next_month_schedule'),
    path(
        'month/<int:category_id>/', MonthScheduleView.as_view(), name='month_schedule'
    ),
    path('month/', MonthScheduleView.as_view(), name='month_schedule'),
    path('week/<int:category_id>/', WeekScheduleView.as_view(), name='week_schedule'),
    path('week/', WeekScheduleView.as_view(), name='week_schedule'),
    path('day/<int:category_id>/', DayScheduleView.as_view(), name='day_schedule'),
    path('day/', DayScheduleView.as_view(), name='day_schedule'),
    path('overdue/<int:category_id>/', OverDueScheduleView.as_view(), name='overdue'),
    path('overdue/', OverDueScheduleView.as_view(), name='overdue'),
    path('uncompletable/', UncompletableScheduleView.as_view(), name='uncompletable'),
    path('no_photo_apporval/', NoPhotoScheduleView.as_view(), name='no_photo_apporval'),
    path('search/', SearchView.as_view(), name='search'),
    path(
        'schedule/<int:pk>/<str:return_url>/',
        ScheduleDetailInfoView.as_view(),
        name='schedule_detail',
    ),
    path(
        'schedule/confirm_completed/<slug:schedule_list>/<str:return_url>/',
        ConfirmScheduleCompletedView.as_view(),
        name='confirm_schedule_completed',
    ),
    path(
        'schedule/confirm_date_changed/<slug:schedule_list>/<str:return_url>/',
        ConfirmScheduleDateChangedView.as_view(),
        name='confirm_date_changed',
    ),
    path(
        'schedule/confirm_cant_complete/<slug:schedule_list>/<str:return_url>/',  # noqa: E501
        ConfirmScheduleCannotBeComplete.as_view(),
        name='confirm_schedule_cant_complete',
    ),
    path('xlsx_report/', XlsxReportDownloadView.as_view(), name='xlsx_report'),
    path(
        'distribute_next_month/',
        DistributeNextMonthSchedules.as_view(),
        name='distribute_next_month',
    ),
    path(
        'next_month_plan_xlsx/',
        XlsxNextMonthDownloadView.as_view(),
        name='next_month_plan_xlsx',
    ),
]
