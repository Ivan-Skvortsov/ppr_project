from rest_framework import serializers

from reports.models import Employee, Schedule


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'date_sheduled',
            'date_completed',
            'access_journal_filled',
            'result_journal_filled',
            'employee1',
            'employee2',
            'employee3',
            'photo',
            'uncompleted',
        ]
