from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=20)
    department = models.CharField(max_length=25)  # TODO: change to choices

    def __str__(self):
        return self.name


class MaintenanceCategory(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.category_name


class Facility(models.Model):
    facility_name = models.CharField(max_length=20)
    maintenance_category = models.ForeignKey(
        MaintenanceCategory,
        on_delete=models.CASCADE,
        related_name='maintenance_category',
        null=True
    )

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
    equipment = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.equipment


class EquipmentMaintenanceRegulation(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='maintenance_regulation'
    )
    regulations = models.TextField()


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
