from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import EmployeeViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'schedules', ScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
