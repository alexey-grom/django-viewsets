# encoding: utf-8

from django.conf.urls import patterns, include
from django.core.urlresolvers import reverse_lazy

from viewsets import views
from viewsets import helpers


class BaseViewSet(object):
    mixin_classes = (views.GenericViewMixin, )

    def get_mixin_classes(self):
        return self.mixin_classes

    def collect_urls(self, *other):
        return other

    def wrap_view(self, view_class):
        kwargs = {'viewset': self}  # weakref.ref?
        view_class = helpers.make_mixin(view_class,
                                        *self.get_mixin_classes())
        return kwargs, view_class

    def get_urls(self):
        urls = self.collect_urls()
        nested = patterns('', *urls)
        return include(nested)

    def reverse(self, name, *args, **kwargs):
        return reverse_lazy(name, args=args, kwargs=kwargs)

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls
