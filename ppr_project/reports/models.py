from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=20)
    department = models.CharField(max_length=25)  # TODO: change to choices

    def __str__(self):
        return self.name


class EquipmentMaintenanceRegulation(models.Model):
    regulations = models.TextField()
    regulation_num = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.regulation_num} | {self.regulations[:20]}...'


class MaintenanceCategory(models.Model):
    category_name = models.CharField(max_length=25)

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

    def __str__(self):
        return self.facility_name


class EquipmentType(models.Model):
    eq_type_name = models.CharField(max_length=30)
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return self.eq_type_name


class Equipment(models.Model):
    equipment = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    maintenance_regulation = models.ForeignKey(
        EquipmentMaintenanceRegulation,
        on_delete=models.PROTECT,
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return self.equipment


class Schedule(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        related_name='equipment_type',
        null=True
    )
    maintenance_type = models.CharField(max_length=10)
    date_sheduled = models.DateField()
    date_completed = models.DateField(auto_now_add=True)
    employee1 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee1',
        null=True
    )
    employee2 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee2',
        null=True
    )
    employee3 = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='employee3',
        null=True,
        blank=True
    )
