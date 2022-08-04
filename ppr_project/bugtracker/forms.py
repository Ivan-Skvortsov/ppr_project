from django import forms
from bugtracker.models import Bug, Comment


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        fields = ('type', 'bug_description', 'screenshot')


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment
        fields = ('text',)
