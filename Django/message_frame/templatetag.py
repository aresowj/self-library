from django import template


@register.assignment_tag
def get_message_class_name(tags):
    return 'danger' if tags == 'error' else tags
