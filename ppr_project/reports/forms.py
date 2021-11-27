from django import forms

from reports.models import Employee, Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('position', 'name')
