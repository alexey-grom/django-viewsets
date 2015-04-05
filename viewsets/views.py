# encoding: utf-8

from django.views.generic.base import ContextMixin


class GenericViewMixin(ContextMixin):
    viewset = None

    def get_context_data(self, **kwargs):
        kwargs['viewset'] = self.viewset
        return super(GenericViewMixin, self).get_context_data(**kwargs)
