# encoding: utf-8

from itertools import chain


def make_mixin(view_class, *mixin_classes, **attrs):
    if mixin_classes:
        return type(view_class.__name__,
                    chain(mixin_classes, (view_class, )),
                    attrs)
    return view_class
