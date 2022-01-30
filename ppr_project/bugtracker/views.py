from tempfile import template
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bugtracker.models import Bug


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    context_object_name = 'bug'
    template_name = 'bugtracker/bug_list.html'
