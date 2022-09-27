from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import EmployeeViewSet, ScheduleViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register('schedules', ScheduleViewSet, basename='schedules')


urlpatterns = [
    path('', include(router.urls)),
]
