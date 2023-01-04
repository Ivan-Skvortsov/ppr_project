from rest_framework import serializers

from reports.models import EquipmentType, Facility, Schedule


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


class ScheduleIDSerializer(serializers.Serializer):

    id = serializers.IntegerField()


class CalendarUpdateSerializer(serializers.Serializer):

    date_sheduled = serializers.DateField(format='%Y-%m%d')
    schedules = ScheduleIDSerializer(many=True)


class FacilitySerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='facility_name')

    class Meta:
        model = Facility
        fields = ['id', 'name']


class EquipmentTypeSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='eqipment_type_name')

    class Meta:
        model = EquipmentType
        fields = ['id', 'name']
