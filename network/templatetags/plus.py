from django import template

register = template.Library()

@register.filter(name='plus')
def plus(value,add):
	return value+add
