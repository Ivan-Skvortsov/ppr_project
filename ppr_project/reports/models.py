from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=20)
    department = models.CharField(max_length=25)  # TODO: change to choices

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = "Работники"

    def __str__(self):
        return self.name


class MaintenanceCategory(models.Model):
    category_name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = "Категории работ"

    def __str__(self):
        return self.category_name


class Facility(models.Model):
    facility_name = models.CharField(max_length=20)
    maintenance_category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True
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
        null=True
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=True
    )
    eqipment_type_name = models.CharField(max_length=30)
    report_template = models.FilePathField(default='/')

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = "Типы оборудования"

    def __str__(self):
        return self.eqipment_type_name


class MaintenanceType(models.Model):
    m_type = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Тип ТО'
        verbose_name_plural = 'Типы ТО'

    def __str__(self):
        return self.m_type


class Schedule(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        related_name='equipment_type_schedule',
        null=True
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.SET_NULL,
        related_name='maintenance_type',
        null=True
    )
    date_sheduled = models.DateField()
    date_completed = models.DateField(blank=True, null=True)
    access_journal_filled = models.BooleanField(default=False)
    result_journal_filled = models.BooleanField(default=False)
    employee1 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee1_schedule',
        null=True,
        blank=True
    )
    employee2 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee2_schedule',
        null=True,
        blank=True
    )
    employee3 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee3_schedule',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Планирование работ'
        verbose_name_plural = 'Планирование работ'
