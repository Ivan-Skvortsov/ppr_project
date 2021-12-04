from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserSignUpForm


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
