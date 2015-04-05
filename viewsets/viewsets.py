# encoding: utf-8

from django.conf.urls import patterns, include, url

from . import views
from . import helpers


class BaseViewSet(object):
    def collect_urls(self, *other):
        return other

    def wrap_view(self, view_class):
        kwargs = {'viewset': self}
        view_class = helpers.make_mixin(view_class,
                                        views.GenericViewMixin,
                                        viewset=self)
        return kwargs, view_class

    def get_urls(self):
        urls = self.collect_urls()
        nested = patterns('', *urls)
        return [url(r'^', include(nested))]

    @property
    def urls(self):
        return self.get_urls()
