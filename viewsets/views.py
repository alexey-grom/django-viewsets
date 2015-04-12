# encoding: utf-8

from django.views.generic import base as base_views
from django.views import generic as generic_views
from django.utils.translation import ugettext_lazy as _

from viewsets import compat
from viewsets import helpers


class GenericViewMixin(base_views.ContextMixin, generic_views.View):
    viewset = None

    def get_context_data(self, **kwargs):
        kwargs['viewset'] = self.viewset
        return super(GenericViewMixin, self).get_context_data(**kwargs)


class GuardViewMixin(GenericViewMixin):
    def dispatch(self, request, *args, **kwargs):
        response = self.viewset.pre_dispatch_request(self, request)
        if response:
            return response
        return super(GuardViewMixin, self).dispatch(request, *args, **kwargs)


class ListView(generic_views.ListView, base_views.TemplateResponseMixin,
               GenericViewMixin):
    def get_template_names(self):
        return helpers.generic_template_names(self.viewset, 'list')


class DetailView(generic_views.DetailView, base_views.TemplateResponseMixin,
                 GenericViewMixin):
    def get_template_names(self):
        return helpers.generic_template_names(self.viewset, 'detail')


class CreateView(compat.MessagesMixin,
                 generic_views.CreateView, base_views.TemplateResponseMixin,
                 GenericViewMixin):
    def get_template_names(self):
        return helpers.generic_template_names(self.viewset, 'create')

    def get_success_url(self):
        return self.viewset.reverse('detail', self.object.pk)

    def form_valid(self, form):
        if self.messages:
            self.messages.success(_('Created successful'))
        return super(CreateView, self).form_valid(form)


class UpdateView(compat.MessagesMixin,
                 generic_views.UpdateView, base_views.TemplateResponseMixin,
                 GenericViewMixin):
    def get_template_names(self):
        return helpers.generic_template_names(self.viewset, 'update')

    def get_success_url(self):
        return self.viewset.reverse('detail', self.object.pk)

    def form_valid(self, form):
        if self.messages:
            self.messages.success(_('Updated successful'))
        return super(UpdateView, self).form_valid(form)


class DeleteView(compat.MessagesMixin,
                 generic_views.DeleteView, base_views.TemplateResponseMixin,
                 GenericViewMixin):
    def get_template_names(self):
        return helpers.generic_template_names(self.viewset, 'delete')

    def get_success_url(self):
        if self.messages:
            self.messages.success(_('Deleted successful'))
        return self.viewset.reverse('list')
