# encoding: utf-8

from django import template
from django.core.urlresolvers import RegexURLPattern

from viewsets import compat, mixins


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

    assert view_name
    assert viewset
    assert request
    assert isinstance(viewset, mixins.PermissionsMixin)

    if not viewset_has(viewset, view_name):
        return False
    return viewset.has_access(view_name, request, obj)


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


@register.inclusion_tag('viewsets/_object.html', takes_context=True)
def viewset_render_object(context, obj):
    viewset = context.get('viewset')

    assert obj
    assert viewset
    assert isinstance(viewset, mixins.ModelSerializeMixin)

    data = viewset.serialize_object(obj)

    return {'fields': data}
