from django.contrib.auth import get_user_model
from django.db import models

from simple_history.models import HistoricalRecords

User = get_user_model()


class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name='Фамилия И.О.')
    position = models.CharField(max_length=50, verbose_name='Должность')
    department = models.CharField(max_length=50, verbose_name='Служба')

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = "Работники"
        ordering = ['department', 'name']

    def __str__(self):
        return f'{self.department} | {self.name}'


class MaintenanceCategory(models.Model):
    category_name = models.CharField(
        max_length=50,
        verbose_name='Категория работ'
    )

    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = "Категории работ"

    def __str__(self):
        return self.category_name


class Facility(models.Model):
    facility_name = models.CharField(max_length=250, verbose_name='Объект')
    maintenance_category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория работ'
        )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = "Объекты"

    def __str__(self):
        return self.facility_name


class EquipmentType(models.Model):
    maintenance_category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Категория работ'
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Объект'
    )
    eqipment_type_name = models.CharField(
        max_length=250,
        verbose_name='Тип оборудования'
    )

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = "Типы оборудования"

    def __str__(self):
        return self.eqipment_type_name


class MaintenanceType(models.Model):
    m_type = models.CharField(max_length=50, verbose_name='Тип ТО')

    class Meta:
        verbose_name = 'Тип ТО'
        verbose_name_plural = 'Типы ТО'

    def __str__(self):
        return self.m_type


class ReportTemplate(models.Model):
    template_name = models.CharField(
        max_length=250,
        verbose_name='Имя шаблона'
    )
    template = models.FileField(upload_to='templates/')

    class Meta:
        verbose_name = 'Шаблон акта/протокола'
        verbose_name_plural = 'Шаблоны актов/протоколов'

    def __str__(self):
        return self.template_name


class UncompleteReasons(models.Model):
    reason = models.CharField(
        max_length=250,
        verbose_name='Причина невыполнения'
    )

    class Meta:
        verbose_name = 'Причина невыполнения работ'
        verbose_name_plural = 'Причины невыполнения работ'

    def __str__(self):
        return self.reason


class Schedule(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        related_name='equipment_type_schedule',
        null=True,
        verbose_name='Тип оборудования'
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.SET_NULL,
        related_name='maintenance_type',
        null=True,
        verbose_name='Тип ТО'
    )
    date_sheduled = models.DateField(verbose_name='Дата по плану')
    date_completed = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата выполнения'
    )
    access_journal_filled = models.BooleanField(
        default=False,
        verbose_name='Журнал допуска заполнен'
    )
    result_journal_filled = models.BooleanField(
        default=False,
        verbose_name='Журнал ТО заполнен'
    )
    employee1 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee1_schedule',
        null=True,
        blank=True,
        verbose_name='Исполнитель #1'
    )
    employee2 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee2_schedule',
        null=True,
        blank=True,
        verbose_name='Исполнитель #2'
    )
    employee3 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee3_schedule',
        null=True,
        blank=True,
        verbose_name='Исполнитель #3'
    )
    report = models.ForeignKey(
        ReportTemplate,
        on_delete=models.SET_NULL,
        related_name='report_template',
        null=True,
        blank=True,
        verbose_name='Шаблон акта/протокола'
    )
    photo = models.ImageField(
        upload_to='photo_approvals/%Y/%m/%d',
        blank=True,
        verbose_name='Подтверждающее фото'
    )
    uncompleted = models.ForeignKey(
        UncompleteReasons,
        on_delete=models.SET_NULL,
        related_name='schedule_uncompleted_reason',
        blank=True,
        null=True,
        verbose_name='Причина невыполнения работы'
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Планирование работ'
        verbose_name_plural = 'Планирование работ'

    def __str__(self):
        return (
            f'{self.equipment_type.maintenance_category} | '
            f'{self.equipment_type.facility} | '
            f'{self.maintenance_type} | {self.equipment_type}'
        )
