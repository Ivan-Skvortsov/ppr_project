# Generated by Django 3.2.7 on 2022-01-26 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_schedule_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='updated_by',
        ),
    ]
