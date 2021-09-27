from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=20)
    department = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Facility(models.Model):
    facility_name = models.CharField(max_length=20)

    def __str__(self):
        return self.facility_name


class EquipmentType(models.Model):
    eq_type_name = models.CharField(max_length=30)
    facility = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        related_name='equipment_type',
        null=True
        )

    def __str__(self):
        return self.eq_type_name


class Equipment(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        related_name='equipment',
        null=True
    )
    equipment = models.CharField(max_length=20, default='-empty-')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.equipment_type

class Job(models.Model):
    asu_engineer = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='asu_engineer',
        null=True
    )
    facility_id = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        null=True
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        null=True
    )
    job_date = models.DateField(auto_now_add=True)
