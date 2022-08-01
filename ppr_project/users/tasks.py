from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER

from celery import shared_task


@shared_task
def send_email_task(subject, message, receivers):
    send_mail(subject, message, EMAIL_HOST_USER, receivers)
