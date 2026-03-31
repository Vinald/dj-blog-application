from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    """Add CSS classes to form field"""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field


@register.filter(name='add_error_class')
def add_error_class(field, css_class):
    """Add error CSS classes to form field if it has errors"""
    if field.errors:
        css_class = f"{css_class} is-invalid"
    return add_class(field, css_class)
