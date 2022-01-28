from django import forms
from django.forms.widgets import CheckboxInput, DateInput, Select

from reports.models import Employee, Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = [
            'equipment_type',
            'maintenance_type',
            'report'
        ]
        widgets = {
            'date_sheduled': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'date_completed': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'employee1': Select(
                attrs={'class': 'form-control form-select'}
            ),
            'employee2': Select(
                attrs={'class': 'form-control form-select'}
            ),
            'employee3': Select(
                attrs={'class': 'form-control form-select'}
            ),
            'access_journal_filled': CheckboxInput(
                attrs={'class': 'form-check-input mt-0'}
            ),
            'result_journal_filled': CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class EmployeeForm(forms.Form):
    qs = Employee.objects.all()
    employee1 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель #1'
    )
    employee2 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель #2'

    )
    employee3 = forms.ModelChoiceField(
        queryset=qs,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель #3'

    )


class DateInputForm(forms.Form):
    input_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label='Дата',
        help_text='Выберите дату'
    )
