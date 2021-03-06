
from decimal import Decimal

from django.template import Library

register = Library()


@register.filter
def as_percent(value, places='0'):
    if value is None: return "-"
    return "{}%".format(
        Decimal(value * 100).quantize(Decimal(places)))

@register.inclusion_tag('analytics/includes/counters.html')
def counters(title, counters):
    return {
        'title': title,
        'counters': counters,
    }
