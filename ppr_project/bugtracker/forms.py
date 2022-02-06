from django import forms
from bugtracker.models import Bug


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        fields = ('type', 'bug_description', 'screenshot', 'close_date', 'author')
