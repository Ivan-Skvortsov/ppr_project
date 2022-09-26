from rest_framework import mixins, viewsets

from api.serializers import EmployeeSerializer, ScheduleSerializer
from reports.models import Employee, Schedule


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ScheduleViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
