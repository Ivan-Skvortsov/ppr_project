from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import UserSignUpForm


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('users:signup_done')
    template_name = 'users/signup.html'


class SignUpDone(TemplateView):
    template_name = 'users/signup_done.html'
