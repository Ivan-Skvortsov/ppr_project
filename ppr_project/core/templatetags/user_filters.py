from datetime import date, timedelta
from django import template

from reports.models import Schedule

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
    """Template tag to count uncompletable schedules for last two months."""
    previous_month = date.today().month - 1
    return Schedule.objects.filter(date_sheduled__month__gte=previous_month,
                                   date_completed__isnull=True,
                                   uncompleted__isnull=False).count()
