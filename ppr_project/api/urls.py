from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import EmployeeViewSet, ScheduleViewSet


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'schedule', ScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
