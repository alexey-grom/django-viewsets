# encoding: utf-8

from django.conf.urls import patterns, include
from django.core.urlresolvers import reverse_lazy

from viewsets import views
from viewsets import helpers


class BaseViewSet(object):
    def __init__(self, **kwargs):
        super(BaseViewSet, self).__init__()
        for key, value in kwargs.iteritems():
            assert hasattr(self, key), 'Pass unknown parameter'
            setattr(self, key, value)

    def get_mixin_classes(self, view_class):
        return (views.GenericViewMixin, )

    def collect_urls(self, *other):
        return other

    def wrap_view(self, view_class):
        kwargs = {'viewset': self}
        view_class = helpers.make_mixin(view_class, *self.get_mixin_classes(view_class))
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
