from django.urls import path
from bugtracker import views


app_name = 'bugtracker'

urlpatterns = [
    path('', views.BugListView.as_view(), name='index'),
]
