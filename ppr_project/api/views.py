import logging
from collections import OrderedDict
from datetime import datetime
from http import HTTPStatus

from rest_framework import exceptions, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CalendarUpdateSerializer, EquipmentTypeSerializer,
                             FacilitySerializer, ScheduleWriteSerializer)
from reports.models import EquipmentType, Facility, Schedule

logger = logging.getLogger(__name__)


class ScheduleViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    DATE_FORMAT = '%Y-%m-%d'
    serializer_class = ScheduleWriteSerializer

    def get_queryset(self):
        queryset = Schedule.objects.all()
        start = self.request.query_params.get('start').split('T')[0]
        end = self.request.query_params.get('end').split('T')[0]
        if start and end:
            start_date = datetime.strptime(start, self.DATE_FORMAT)
            end_date = datetime.strptime(end, self.DATE_FORMAT)
            queryset = queryset.filter(date_sheduled__range=[start_date, end_date])
        return queryset

    @action(methods=['GET'], detail=False, url_path='get_calendar')
    def get_calendar_data(self, request):
        colors = {  # FIXME - вынести в настроки
            'АСУ ПТК': '#0e432a',
            'СВТ': '#198754',
            'ППР АСПСиКЗ КЦ-2': '#dc3545',
            'ППР АСПСиКЗ КЦ-1': '#dc3545',
            'ППР защит КЦ-2': '#6610f2',
            'ППР защит КЦ-1': '#6610f2',
            'ППР ПБ': '#044ab2',
            'ППР КЦ-2': '#0d6efd',
            'ППР КЦ-1': '#0d6efd'
        }
        queryset = self.get_queryset().values(
            'equipment_type__facility__maintenance_category__category_name',
            'equipment_type__facility__id',
            'equipment_type__facility__facility_name',
            'equipment_type__eqipment_type_name',
            'maintenance_type__m_type',
            'date_sheduled',
            'id'
        )
        regrouped_queryset = OrderedDict()
        for entry in queryset:
            regrouped_queryset.setdefault(
                (
                    entry['date_sheduled'],
                    entry['equipment_type__facility__id'],
                    entry['equipment_type__facility__facility_name'],
                    entry['equipment_type__facility__maintenance_category__category_name']
                ), list()
            ).append(
                {
                    'maintenance_type': entry['maintenance_type__m_type'],
                    'equipment_type': entry['equipment_type__eqipment_type_name'],
                    'id': entry['id']
                }
            )
        output_data = [
            {
                'start': key[0],
                'id': key[1],
                'title': key[2],
                'backgroundColor': colors[key[3]],
                'schedules': value
            } for key, value in regrouped_queryset.items()
        ]
        return Response(output_data)

    @action(methods=['POST'], detail=False, url_path='bulk_update')
    def bulk_update_date_sheduled_values(self, request):
        serializer = CalendarUpdateSerializer(data=request.data)
        if serializer.is_valid():
            date_sheduled = serializer.validated_data.get('date_sheduled')
            schedule_ids = [schedule.get('id') for schedule in serializer.validated_data['schedules']]
            if not (date_sheduled and schedule_ids):
                raise exceptions.ValidationError('Incorrect value for date_sheduled or shedules!')
            try:
                shedules = Schedule.objects.filter(id__in=schedule_ids)
                shedules.update(date_sheduled=date_sheduled)
            except Exception as e:
                logger.error(f'Error updating from calendar: {e}')
                raise exceptions.APIException('Incorrect data')
            return Response(status=HTTPStatus.OK)
        raise exceptions.APIException('Incorrect data')


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
