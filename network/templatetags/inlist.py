from django import template

register = template.Library()

@register.filter(name='is_in')
def is_in(element, thelist):
    return element in thelist
