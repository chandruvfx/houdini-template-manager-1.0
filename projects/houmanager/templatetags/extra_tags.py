from django import template

register = template.Library()

@register.filter()
def t_rsplit(value):
    return value.rsplit('_',1)[0]

@register.filter()
def version(value):
    return f"v{str(value).zfill(3)}"