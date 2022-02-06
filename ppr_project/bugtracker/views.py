from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bugtracker.models import Bug
from bugtracker.forms import BugForm
from django.urls import reverse_lazy


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    context_object_name = 'bug'
    template_name = 'bugtracker/bug_list.html'


class BugCreateView(LoginRequiredMixin, CreateView):
    form_class = BugForm
    model = Bug
    template_name = 'bugtracker/bug_create.html'
    success_url = reverse_lazy('bugtracker:index')
