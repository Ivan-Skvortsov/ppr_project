from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from bugtracker.forms import BugForm, CommentForm
from bugtracker.models import Bug, Comment


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    context_object_name = 'bugs'
    template_name = 'bugtracker/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BugForm()
        return context


class BugCreateView(LoginRequiredMixin, CreateView):
    form_class = BugForm
    model = Bug
    success_url = reverse_lazy('bugtracker:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = date.today()
        return super().form_valid(form)


class BugDetailView(LoginRequiredMixin, DetailView):
    template_name = 'bugtracker/bug_detail.html'
    model = Bug
    context_object_name = 'bug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bug = self.get_object()
        context['comment_form'] = CommentForm()
        context['bug_comments'] = bug.comments.all()
        return context


class AddCommentView(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.bug = get_object_or_404(Bug, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bugtracker:detail', kwargs={'pk': self.kwargs['pk']})


class CloseBug(UserPassesTestMixin, View):
    """
    Close bug. Closing bug means that close_date field of Bug model is
    set to now(). Allowed only to staff users.
    """

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, **kwargs):
        bug = get_object_or_404(Bug, pk=self.kwargs['pk'])
        bug.close_date = date.today()
        bug.save()
        return redirect('bugtracker:detail', kwargs['pk'])
