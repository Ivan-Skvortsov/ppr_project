from django.urls import path

from reports.views import (ConfirmScheduleCannotBeComplete,
                           ConfirmScheduleCompletedView,
                           ConfirmScheduleDateChangedView,
                           DateRangeScheduleView, DistributeNextMonthSchedules,
                           IndexView, NoPhotoScheduleView, OverDueScheduleView,
                           PhotoApprovalsDownloadView, ScheduleCreateView,
                           ScheduleDetailInfoView, SearchView,
                           SelectDateRangeForScheduleView,
                           UncompletableScheduleView,
                           XlsxNextMonthDownloadView, XlsxReportDownloadView)

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('overdue/<int:category_id>/', OverDueScheduleView.as_view(), name='overdue'),
    path('overdue/', OverDueScheduleView.as_view(), name='overdue'),
    path('uncompletable/', UncompletableScheduleView.as_view(), name='uncompletable'),
    path('no_photo_apporval/', NoPhotoScheduleView.as_view(), name='no_photo_apporval'),
    path('search/', SearchView.as_view(), name='search'),
    path('select_date_range/', SelectDateRangeForScheduleView.as_view(), name='select_date_range'),
    path('schedule/<int:pk>/', ScheduleDetailInfoView.as_view(), name='schedule_detail'),
    path('schedule/confirm_completed/', ConfirmScheduleCompletedView.as_view(), name='confirm_schedule_completed'),
    path('schedule/confirm_date_changed/', ConfirmScheduleDateChangedView.as_view(), name='confirm_date_changed'),
    path(
        'schedule/confirm_cant_complete/',
        ConfirmScheduleCannotBeComplete.as_view(),
        name='confirm_schedule_cant_complete'
    ),
    path('xlsx_report/', XlsxReportDownloadView.as_view(), name='xlsx_report'),
    path('photo_approvals/', PhotoApprovalsDownloadView.as_view(), name='photo_apporvals'),
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
    path('create/', ScheduleCreateView.as_view(), name='create_schedule'),
    path('schedules/<slug:start_date>/<slug:end_date>/', DateRangeScheduleView.as_view(), name='date_range'),
]
