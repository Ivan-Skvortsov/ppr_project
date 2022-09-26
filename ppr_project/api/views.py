from rest_framework import mixins, permissions, viewsets

from api.serializers import (
    EmployeeSerializer,
    ScheduleSerializer,
    ScheduleWriteSerializer,
)
from reports.models import Employee, Schedule


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ScheduleViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ScheduleSerializer
        return ScheduleWriteSerializer
