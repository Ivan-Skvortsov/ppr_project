from django.db import models
from django.db.models.fields import CharField


class Employee(models.Model):
    name = CharField(max_length=30, null=False, blank=False)
    position = CharField(max_length=20, null=False, blank=False)
    department = CharField(max_length=15, null=False, blan=False)


# class Equipment(models.Model):
    

# class Facility(models.Model):
#     name = CharField(max_length=15, null=False, blank=True, unique=True)
#     equipment_type = CharField(max_length=10, null=False, blank=False)
#     equipment_type_maintenance_period = 