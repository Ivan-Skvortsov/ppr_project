from datetime import date

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from bugtracker.models import Bug
from bugtracker.forms import BugForm


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    context_object_name = 'bugs'
    template_name = 'bugtracker/bug_list.html'


class BugCreateView(LoginRequiredMixin, CreateView):
    form_class = BugForm
    model = Bug
    template_name = 'bugtracker/bug_create.html'
    success_url = reverse_lazy('bugtracker:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = date.today()
        return super().form_valid(form)
