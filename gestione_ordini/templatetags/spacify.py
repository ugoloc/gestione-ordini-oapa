from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = Library()

@stringfilter
def spacify(value, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	#value = mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
	#return mark_safe(re.sub('\n', esc('<br />'), esc(value)))
	value = esc(value)
	value = mark_safe(value.replace('  ', ' &nbsp;'))
	return mark_safe(value.replace('\n', '<br />'))
spacify.needs_autoescape = True
register.filter(spacify)