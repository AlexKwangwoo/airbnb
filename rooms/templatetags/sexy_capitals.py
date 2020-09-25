from django import template

register = template.Library()


@register.filter  # (name="하고싶은이름") 하면 메소드 이름 하고싶은이름 하면됨!
def sexy_capitals(value):
    return value.capitalize()
