from django.template import Library
from utils import formater, utils

register = Library()

@register.filter
def format_price(value):
    return formater.format_price(value)

@register.filter
def total_cart_qty(cart):
    return utils.total_cart_qty(cart)

@register.filter
def total_cart_price(cart):
    return utils.total_cart_price(cart)