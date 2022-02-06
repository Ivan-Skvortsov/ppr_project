from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

BUG_TYPE_CHOICES = [
    ('BG', 'Замечание'),
    ('FT', 'Предложение')
]


class Bug(models.Model):
    type = models.CharField(
        max_length=150,
        choices=BUG_TYPE_CHOICES,
        verbose_name='Тип',
        help_text='Выберите тип'
    )
    bug_description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание'
    )
    screenshot = models.ImageField(
        upload_to='bugtracker/%Y/%m/%d',
        blank=True,
        verbose_name='Скриншот или фото'
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    close_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата устранения/внедрения'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        null=True,
        blank=True
    )
