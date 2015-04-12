# encoding: utf-8

from django.views.generic import base as base_views
from django.views import generic as generic_views


class GenericViewMixin(base_views.ContextMixin):
    viewset = None

    def get_context_data(self, **kwargs):
        kwargs['viewset'] = self.viewset
        return super(GenericViewMixin, self).get_context_data(**kwargs)


class TemplateMixin(base_views.TemplateResponseMixin, base_views.ContextMixin):
    model = None
    generic_name = None

    def get_template_names(self):
        result = super(TemplateMixin, self).get_template_names()

        if self.generic_name:
            result = ['viewsets/{}.html'.format(self.generic_name)] + result

        if self.model and self.generic_name:
            opts = self.model._meta
            args = dict(app=opts.app_label,
                        model=opts.model_name,
                        generic_name=self.generic_name)
            result = ['{app}/{model}/{generic_name}.html'.format(**args),
                      '{app}/{generic_name}.html'.format(**args),
                      '{generic_name}.html'.format(**args), ] + result

        return result

    def get_context_data(self, **kwargs):
        if self.model:
            kwargs['model_meta'] = self.model._meta
        return super(TemplateMixin, self).get_context_data(**kwargs)


class ListView(TemplateMixin, GenericViewMixin, generic_views.ListView):
    generic_name = 'list'


class DetailView(TemplateMixin, GenericViewMixin, generic_views.DetailView):
    generic_name = 'detail'


class CreateView(TemplateMixin, GenericViewMixin, generic_views.CreateView):
    generic_name = 'create'

    def get_success_url(self):
        return self.viewset.reverse('detail', self.object.pk)


class UpdateView(TemplateMixin, GenericViewMixin, generic_views.UpdateView):
    generic_name = 'update'

    def get_success_url(self):
        return self.viewset.reverse('detail', self.object.pk)


class DeleteView(TemplateMixin, GenericViewMixin, generic_views.DeleteView):
    generic_name = 'delete'

    def get_success_url(self):
        return self.viewset.reverse('list')
