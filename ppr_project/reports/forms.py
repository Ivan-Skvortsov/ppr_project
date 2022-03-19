from django import forms
from django.forms.widgets import CheckboxInput, DateInput, Select, ClearableFileInput
from django.core.validators import MinValueValidator
from datetime import date

from reports.models import Employee, Schedule, MaintenanceCategory, MaintenanceType


class CustomFileInput(ClearableFileInput):
    template_name = 'reports/widgets/custom_file_input.html'


class ScheduleForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        date_completed = cleaned_data.get("date_completed")
        employee1 = cleaned_data.get("employee1")
        employee2 = cleaned_data.get("employee2")
        if date_completed and not(employee1 and employee2):
            raise forms.ValidationError(
                    'Нельзя указать, что работа завершена без исполнителей! '
                    'Выберите как минимум двух исполнителей работы!'
                )
        return cleaned_data

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
            ),
            'photo': CustomFileInput(
                attrs={'class': 'form-control'}
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
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today
            }
        ),
        label='Дата',
        help_text='Выберите дату',
        validators=[MinValueValidator(date.today)]
    )


class ScheduleSearchForm(forms.Form):
    equipment_type__maintenance_category__pk = forms.ModelChoiceField(
        queryset=MaintenanceCategory.objects.all().order_by('pk'),
        required=False,
        label='Категория'
    )
    equipment_type__facility__facility_name__icontains = forms.CharField(
        max_length=300,
        required=False,
        label='Объект'
    )
    equipment_type__eqipment_type_name__icontains = forms.CharField(
        max_length=300,
        required=False,
        label='Наименование оборудования'
    )
    maintenance_type__pk = forms.ModelChoiceField(
        queryset=MaintenanceType.objects.all().order_by('m_type'),
        required=False,
        label='Вид ТО'
    )
    date_sheduled__gte = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='С даты'
    )
    date_sheduled__lte = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='По дату'
    )
    date_completed__gte = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='С даты'
    )
    date_completed__lte = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='По дату'
    )
