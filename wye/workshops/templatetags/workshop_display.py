from django import template

register = template.Library()


@register.inclusion_tag('workshops/workshop_display.html')
def show_workshops(workshops):

    return {'workshop': workshops}
