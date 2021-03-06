from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def edit_links(item, user, approve_label, edit_label):
    elements = []
    if item.can_be_approved_by(user):
        elements.append('<a href="%s">%s</a>' % (item.get_approve_url(), approve_label))
    if item.can_be_edited_by(user):
        elements.append('<a href="%s">%s</a>' % (item.get_edit_url(), edit_label))
    return mark_safe(" | ".join(elements))
