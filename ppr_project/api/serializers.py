from rest_framework import serializers

from reports.models import EquipmentType, Facility, Schedule


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


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'facility_name']


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'eqipment_type_name']
