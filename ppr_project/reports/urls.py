from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('year/', views.YearScheduleView.as_view(), name='year_schedule'),
    path('month/', views.MonthScheduleView.as_view(), name='month_schedule')
]
