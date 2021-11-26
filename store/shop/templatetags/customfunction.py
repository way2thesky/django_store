from django import template

register = template.Library()

shippingConst = 100


@register.filter(name='shipping')
def shipping(value):
    return shippingConst


@register.filter(name='payabletotal')
def payabletotal(value):
    return value + shippingConst


@register.filter(name='subtotal')
def subtotal(value, args):
    return value * args
