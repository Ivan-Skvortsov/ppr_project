from django import forms

from reports.models import Employee, Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'


class EmployeeForm(forms.Form):
    qs = Employee.objects.all()
    employee1 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель №1'
    )
    employee2 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель №2'

    )
    employee3 = forms.ModelChoiceField(
        queryset=qs,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
            }
        ),
        label='Исполнитель №3'

    )


class DateInputForm(forms.Form):
    input_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label='Дата',
        help_text='Выберите дату'
    )
