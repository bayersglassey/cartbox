
from decimal import Decimal

from django.template import Library

register = Library()


@register.filter
def as_percent(value, places='0'):
    return "{}%".format(
        Decimal(value * 100).quantize(Decimal(places)))

@register.inclusion_tag('analytics/includes/samples.html')
def samples(title, samples):
    return {
        'title': title,
        'samples': samples,
    }
