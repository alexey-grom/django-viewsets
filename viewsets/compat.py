# encoding: utf-8

try:
    import crispy_forms
    from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
except ImportError:
    crispy_forms = None
    as_crispy_form = None

try:
    import django_filters
except ImportError:
    django_filters = None

try:
    import braces.views as braces
except ImportError:
    braces = None


if braces:
    MessagesMixin = braces.MessageMixin
else:
    class MessagesMixin(object):
        messages = None
