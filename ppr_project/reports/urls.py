from django.urls import path

from reports.views import IndexView, YearScheduleView, MonthScheduleView, DayScheduleView, ApplyActionToSelectedSchedules

app_name = 'reports'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('year/', YearScheduleView.as_view(), name='year_schedule'),
    path('month/', MonthScheduleView.as_view(), name='month_schedule'),
    path('day/', DayScheduleView.as_view(), name='day_schedule'),
    path(
        'apply_action/',
        ApplyActionToSelectedSchedules.as_view(),
        name='apply_actions'
    )
]
