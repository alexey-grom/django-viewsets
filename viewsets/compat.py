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
    import braces
except ImportError:
    django_filters = None
