from django.template import Library
from utils import format

register = Library()

@register.filter
def format_price(value):
    return format.format_price(value)