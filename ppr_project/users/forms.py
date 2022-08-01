from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from users.tasks import send_email_task

User = get_user_model()


class UserSignUpForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label='Email адрес'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def save(self):
        user = super().save(commit=False)
        user.is_active = False
        user.save()
        subject = 'New user signed up!'
        message = ('New user signed up on KS45 PPR PROJECT SYSTEM: '
                   f'{user.get_full_name()}!')
        admin_mailboxes = [a[1] for a in settings.ADMINS]
        send_email_task.delay(subject, message, admin_mailboxes)
        return user
