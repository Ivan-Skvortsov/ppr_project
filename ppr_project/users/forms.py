from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins

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
        mail_admins(
            subject='New user signed up!',
            message=('New user signed up on KS45 PPR PROJECT SYSTEM: '
                     f'{user.get_full_name()}!')
        )
        return user
