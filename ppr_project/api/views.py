from rest_framework import mixins, permissions, viewsets

from api.serializers import (EquipmentTypeSerializer, FacilitySerializer,
                             ScheduleSerializer, ScheduleWriteSerializer)
from reports.models import EquipmentType, Facility, Schedule


class ScheduleViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Schedule.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ScheduleSerializer
        return ScheduleWriteSerializer


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = FacilitySerializer

    def get_queryset(self):
        queryset = Facility.objects.all()
        maintenance_category = self.request.query_params.get('maintenance_category')
        if maintenance_category is not None:
            queryset = queryset.filter(maintenance_category=maintenance_category)
        return queryset


class EquipmentTypeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = EquipmentTypeSerializer

    def get_queryset(self):
        queryset = EquipmentType.objects.all()
        facility = self.request.query_params.get('facility')
        if facility is not None:
            queryset = queryset.filter(facility=facility)
        return queryset
