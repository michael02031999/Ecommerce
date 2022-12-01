from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def update_variable(val=None):
    """Allows to update existing variable in template"""
    return val
