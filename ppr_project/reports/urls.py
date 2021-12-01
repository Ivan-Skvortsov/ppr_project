from django.urls import path

from reports.views import (ConfirmScheduleAction,
                           IndexView,
                           YearScheduleView,
                           MonthScheduleView,
                           WeekScheduleView,
                           DayScheduleView,
                           ScheduleDetailInfo)

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('year/', YearScheduleView.as_view(), name='year_schedule'),
    path('month/', MonthScheduleView.as_view(), name='month_schedule'),
    path('week/', WeekScheduleView.as_view(), name='week_schedule'),
    path('day/', DayScheduleView.as_view(), name='day_schedule'),
    path(
        'schedule/<int:pk>/',
        ScheduleDetailInfo.as_view(),
        name='schedule_detail'
    ),
    path(
        'schedule/confirm/<slug:schedule_list>/<str:return_page>/',
        ConfirmScheduleAction.as_view(),
        name='confirm_schedule_action')
]
