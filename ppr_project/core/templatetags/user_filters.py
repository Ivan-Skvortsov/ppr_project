from calendar import monthrange
from datetime import date, timedelta

from django import template

from reports.models import MaintenanceCategory, Schedule

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def count_overdue_schedules():
    lte_date = date.today() - timedelta(days=1)
    return Schedule.objects.filter(date_sheduled__lte=lte_date,
                                   date_completed=None,
                                   uncompleted=None).count()


@register.simple_tag
def count_uncompletable_schedules():
    """Template tag to count uncompletable schedules for last three months."""
    date_gte = date.today() - timedelta(days=60)
    return Schedule.objects.filter(
        date_sheduled__gte=date_gte,
        date_completed__isnull=True,
        uncompleted__reason__icontains='магистраль').count()


@register.simple_tag
def count_schedules_without_photo_approvals():
    """Counts completed schedules with no photo approvals attached."""
    return Schedule.objects.filter(
        date_completed__isnull=False,
        photo='',
        maintenance_type__m_type__icontains='Проверка'
    ).count()


@register.simple_tag
def current_day_date_range():
    """Gets todays dates."""
    today = date.today()
    return today, today


@register.simple_tag
def current_week_date_range():
    """Gets dates for start and end of the week."""
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    return start_date, end_date


@register.simple_tag
def current_month_date_range():
    """Gets dates for start and end of the current month."""
    today = date.today()
    days_in_month = monthrange(today.year, today.month)[1]
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month, days_in_month)
    return start_date, end_date


@register.simple_tag
def next_month_date_range():
    """Gets dates for start and end of the next month."""
    current_month = date.today().month
    next_month = current_month % 12 + current_month
    next_month_year = int(date.today().year + (current_month / 12))
    days_in_month = monthrange(next_month_year, next_month)[1]
    start_date = date(next_month_year, next_month, 1)
    end_date = date(next_month_year, next_month, days_in_month)
    return start_date, end_date


@register.simple_tag
def get_maintenance_categories():
    return MaintenanceCategory.objects.all()
