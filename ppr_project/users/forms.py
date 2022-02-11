from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserSignUpForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label='Email адрес'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
