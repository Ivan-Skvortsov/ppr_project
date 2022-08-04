from django.db import models
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.conf import settings

from users.tasks import send_email_task


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

    class Meta:

        ordering = ['-pub_date']
        verbose_name = 'Замечание/предложение'
        verbose_name_plural = 'Замечания/предложения'

    def __str__(self):
        return f'{self.get_type_display()}: {self.bug_description[:20]}...'


class Comment(models.Model):

    bug = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        verbose_name='Предложение/замечание',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        help_text='Введите текст комментария',
        verbose_name='Текст комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария'
    )

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text[:20]}...'


@receiver(signals.post_save, sender=Bug)
def notify_admins_bug_entry_created(sender, instance, created, **kwargs):
    if created:
        subject = 'New bug/feature submitted!'
        message = ('Hello! We have got a new bug entry at ks45.online: \n'
                   f'Pub date: {instance.pub_date}\n'
                   f'Type: {instance.get_type_display()}\n'
                   f'Author: {instance.author.username}\n'
                   f'Description: {instance.bug_description}\n'
                   f'Check it out here: https://ks45.online/bugs/')
        admin_mailboxes = [a[1] for a in settings.ADMINS]
        send_email_task.delay(subject, message, admin_mailboxes)


@receiver(signals.post_save, sender=Comment)
def notify_user_bug_entry_commented(sender, instance, created, **kwargs):
    if created and instance.bug.author != instance.author:
        bug_author = instance.bug.author
        subject = 'Новый комментарий к твоему замечанию в ППР КС-45'
        message = (
            f'Привет {bug_author.username}!\n'
            f'Твое {instance.bug.get_type_display()} прокомментировали.\n'
            f'Автор комментария: {instance.author.username}\n'
            f'Текст комментария: {instance.text}\n'
            f'Подробнее тут: https://ks45.online/bugs/{instance.bug.pk}/')
        send_email_task.delay(subject, message, [bug_author.email])


@receiver(signals.post_save, sender=Bug)
def notify_user_bug_closed(sender, instance, created, **kwargs):
    if instance.close_date is not None:
        subject = f'{instance.get_type_display()} выполнено в ППР КС-45'
        message = (f'Привет {instance.author.username}!\n'
                   'Отличные новости!\n'
                   f'{instance.get_type_display()}, которое ты оставлял в '
                   'системе управления ППР КС-45, отмечено как выполненное.\n'
                   f'Подробнее тут: https://ks45.online/bugs/{instance.pk}/')
        send_email_task.delay(subject, message, [instance.author.email])
