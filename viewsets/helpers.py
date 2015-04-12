# encoding: utf-8

import re
from itertools import chain


CAMELCASE_TO_DASH = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')


def make_mixin(view_class, *mixin_classes, **attrs):
    mixin_classes = filter(lambda Mixin: not issubclass(view_class, Mixin),
                           mixin_classes)
    return type(view_class.__name__,
                tuple(chain(mixin_classes, (view_class, ))),
                attrs)


def camelcase_to_dash(value):
    return CAMELCASE_TO_DASH.\
        sub('-\\1', value).\
        lower().\
        strip('-')


def generic_template_names(viewset, generic_name):
    opts = viewset.model_options
    args = dict(app=opts.app_label,
                model=opts.model_name,
                generic_name=generic_name)
    return ('{app}/{model}/{generic_name}.html'.format(**args),
            '{app}/{generic_name}.html'.format(**args),
            '{generic_name}.html'.format(**args),
            'viewsets/{}.html'.format(generic_name), )
