from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import mail_admins


User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='register_user')
def create_user_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = False
        instance.save()
        new_user_fullname = instance.get_full_name()
        mail_admins(
            subject='New user signed up!',
            message=('New user signed up on KS45 PPR PROJECT SYSTEM: '
                     f'{new_user_fullname}!')
        )


@receiver(post_save, sender=User, dispatch_uid='user_active')
def notify_user_became_active(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        user_full_name = instance.get_full_name()
        subject = 'Аккаунт одобрен!'
        message = (f'Привет {user_full_name}! Отличные новости: твой аккаунт'
                   ' в системе управления ППР КС-45 одобрен!'
                   ' Можешь заходить, используя свой логин и пароль.\n'
                   'На всякий случай (если ты забыл), твой логин - '
                   f'{instance.get_username()}\nСпасибо, что ты с нами!')
        instance.email_user(subject, message)
