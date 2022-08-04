from django.urls import path
from bugtracker import views


app_name = 'bugtracker'

urlpatterns = [
    path('', views.BugListView.as_view(), name='index'),
    path('create/', views.BugCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BugDetailView.as_view(), name='detail'),
    path('<int:pk>/comment/', views.AddCommentView.as_view(), name='comment'),
    path('<int:pk>/close/', views.CloseBug.as_view(), name='close'),
]
