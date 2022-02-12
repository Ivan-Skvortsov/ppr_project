# Generated by Django 3.2.12 on 2022-02-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmenttype',
            name='eqipment_type_name',
            field=models.CharField(max_length=100, verbose_name='Тип оборудования'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_name',
            field=models.CharField(max_length=100, verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='maintenancetype',
            name='m_type',
            field=models.CharField(max_length=15, verbose_name='Тип ТО'),
        ),
    ]
