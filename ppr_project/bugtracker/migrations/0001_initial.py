# Generated by Django 3.2.7 on 2022-01-30 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BG', 'Замечание'), ('FT', 'Предложение')], help_text='Выберите тип', max_length=150, verbose_name='Тип')),
                ('bug_description', models.TextField(help_text='Введите описание', verbose_name='Описание')),
                ('screenshot', models.ImageField(blank=True, upload_to='bugtracker/%Y/%m/%d', verbose_name='Скриншот или фото')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
                ('close_date', models.DateField(blank=True, verbose_name='Дата устранения/внедрения')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
