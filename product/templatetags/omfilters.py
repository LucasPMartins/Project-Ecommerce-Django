from django.template import Library

register = Library()

@register.filter
def format_price(value):
    return f'R$ {value:.2f}'.replace('.', ',')