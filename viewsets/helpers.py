# encoding: utf-8

import re
from itertools import chain


CAMELCASE_ToO_DASH = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')


def make_mixin(view_class, *mixin_classes, **attrs):
    if mixin_classes:
        return type(view_class.__name__,
                    tuple(chain(mixin_classes, (view_class, ))),
                    attrs)
    return view_class


def camelcase_to_dash(value):
    return CAMELCASE_ToO_DASH.\
        sub('-\\1', value).\
        lower().\
        strip('-')
