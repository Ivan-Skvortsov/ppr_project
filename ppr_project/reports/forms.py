from datetime import date

from django import forms
from django.core.validators import MinValueValidator
from django.forms.widgets import (CheckboxInput, ClearableFileInput, DateInput,
                                  Select)

from reports.models import (Employee, MaintenanceCategory, MaintenanceType,
                            Schedule, UncompleteReasons)


class CustomFileInput(ClearableFileInput):
    template_name = 'reports/widgets/custom_file_input.html'


class ScheduleForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        date_completed = cleaned_data.get('date_completed')
        employee1 = cleaned_data.get('employee1')
        employee2 = cleaned_data.get('employee2')
        employee3 = cleaned_data.get('employee3')
        if date_completed and not (employee1 and employee2):
            raise forms.ValidationError(
                'Нельзя указать, что работа завершена без исполнителей! '
                'Выберите как минимум двух исполнителей работы!'
            )
        if len(set([employee1, employee2, employee3])) != 3:
            raise forms.ValidationError('Нельзя указать одинаковых исполнителей!')
        return cleaned_data

    class Meta:
        model = Schedule
        exclude = ['equipment_type', 'maintenance_type', 'report']
        widgets = {
            'date_sheduled': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
            'date_completed': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
            'employee1': Select(attrs={'class': 'form-control form-select'}),
            'employee2': Select(attrs={'class': 'form-control form-select'}),
            'employee3': Select(attrs={'class': 'form-control form-select'}),
            'access_journal_filled': CheckboxInput(attrs={'class': 'form-check-input mt-0'}),
            'result_journal_filled': CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': CustomFileInput(attrs={'class': 'form-control', 'id': 'photo_approval'}),
            'uncompleted': Select(attrs={'class': 'form-control form-select'})
        }


class CompleteScheduleForm(forms.Form):
    qs = Employee.objects.all()
    date_completed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today}),
        label='Дата выполнения работы',
        help_text='Выберите дату выполнения',
    )
    employee1 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='Исполнитель #1'
    )
    employee2 = forms.ModelChoiceField(
        queryset=qs,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='Исполнитель #2'
    )
    employee3 = forms.ModelChoiceField(
        queryset=qs,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='Исполнитель #3'
    )

    def clean(self):
        cleaned_data = super().clean()
        employee1 = cleaned_data.get('employee1')
        employee2 = cleaned_data.get('employee2')
        employee3 = cleaned_data.get('employee3')
        if not employee1 and not employee2:
            raise forms.ValidationError(
                'Нельзя указать, что работа завершена без исполнителей! '
                'Выберите как минимум двух исполнителей работы!'
            )
        if len(set([employee1, employee2, employee3])) != 3:
            raise forms.ValidationError('Нельзя указать одинаковых исполнителей!')
        return cleaned_data


class UncompleteReasonForm(forms.Form):
    reason = forms.ModelChoiceField(
        queryset=UncompleteReasons.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='Причина невыполнения работы'
    )


class DateInputForm(forms.Form):
    input_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today}),
        label='Дата',
        help_text='Выберите дату',
        validators=[MinValueValidator(date.today)]
    )


class ReportDownloadForm(forms.Form):
    report_type = forms.ChoiceField(
        choices=[
            ('ppr', 'Протокол ППР'),
            ('ppz', 'Протокол проверки защит'),
            ('asps', 'Отчет по АСПС для пожарных')
        ],
        initial='ppr',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Тип протокола',
        help_text='Выберите тип протокола'
    )
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Начало периода',
        help_text='Выберите дату',
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Конец периода',
        help_text='Выберите дату',
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from > date_to:
            raise forms.ValidationError('Начало периода не может быть позже конца периода!')
        return cleaned_data


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
