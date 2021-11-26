from django import template


register = template.Library()


@register.filter
def get_list_item(list_, idx):
    return list_[idx]
