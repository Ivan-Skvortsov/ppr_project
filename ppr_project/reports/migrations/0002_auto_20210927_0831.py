# Generated by Django 3.2.7 on 2021-09-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='equipment',
            field=models.CharField(default='-empty-', max_length=20),
        ),
        migrations.AddField(
            model_name='equipment',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
