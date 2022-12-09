from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import EquipmentTypeViewSet, FacilityViewSet, ScheduleViewSet

app_name = 'api'

router = DefaultRouter()
router.register('schedules', ScheduleViewSet, basename='schedules')
router.register('facilities', FacilityViewSet, basename='facilities')
router.register('equipment_types', EquipmentTypeViewSet, basename='equipment_types')


urlpatterns = [
    path('', include(router.urls)),
]
