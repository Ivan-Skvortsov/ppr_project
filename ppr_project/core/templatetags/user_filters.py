from datetime import date
from django import template

from reports.models import Schedule

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def count_overdue_schedules():
    today_date = date.today()
    return Schedule.objects.filter(date_sheduled__lte=today_date,
                                   date_completed=None).count()
