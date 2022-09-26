from rest_framework import viewsets

from api.serializers import EmployeeSerializer, ScheduleSerializer
from reports.models import Employee, Schedule


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ScheduleViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.all()[:30]
    serializer_class = ScheduleSerializer
