# encoding: utf-8

from collections import OrderedDict

from django import template
from django.core.urlresolvers import RegexURLPattern

from viewsets import compat


register = template.Library()


@register.filter
def viewset_has(viewset, view_name):
    for pattern in viewset.urls[0]:
        if isinstance(pattern, RegexURLPattern):
            if pattern.name == view_name:
                return True
    return False


@register.assignment_tag(takes_context=True)
def viewset_has_permission(context, view_name, obj=None):
    request = context.get('request')
    viewset = context.get('viewset')
    if not viewset_has(viewset, view_name):
        return False
    if not hasattr(viewset, 'is_has_permission'):
        return True
    return viewset.is_has_permission(request, view_name, obj)


@register.simple_tag(takes_context=True)
def viewset_reverse(context, *args, **kwargs):
    viewset = context['viewset']
    assert viewset is not None
    return viewset.reverse(*args, **kwargs)


@register.simple_tag
def viewset_render_form(form, *args, **kwargs):
    if compat.as_crispy_form:
        return compat.as_crispy_form(form, *args, **kwargs)
    else:
        return form.as_table()


@register.inclusion_tag('viewsets/_object.html')
def viewset_render_object(object):
    options = object.__class__._meta
    data = OrderedDict([
        (field.verbose_name, getattr(object, field.name))
        for field in options.get_fields()
    ])
    return {'fields': data}
