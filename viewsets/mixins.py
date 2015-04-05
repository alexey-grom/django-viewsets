# encoding: utf-8

from django.conf.urls import url
from django.views import generic as generic_views

from . import viewsets
from . import helpers


class ModelNamespaceMixin(viewsets.BaseViewSet):
    model = None

    def get_namespace(self):
        namespace = super(ModelNamespaceMixin, self).get_namespace()
        if namespace is None and self.model:
            namespace = helpers.camelcase_to_dash(self.model.__name__)
        return namespace


class ListMixin(viewsets.BaseViewSet):
    model = None
    queryset = None
    list_template_name = None
    paginate_by = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_list_view()
        item = url('^$',
                   view_class.as_view(**kwargs),
                   name='list')
        return super(ListMixin, self).collect_urls(item, *other)

    def build_list_view(self):
        kwargs, view_class = self.wrap_view(generic_views.ListView)
        kwargs.update({
            'template_name': self.list_template_name,
            'model': self.model,
            'queryset': self.queryset,
            'paginate_by': self.paginate_by,
        })
        return kwargs, view_class


class DetailMixin(viewsets.BaseViewSet):
    model = None
    queryset = None
    detail_template_name = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_detail_view()
        item = url('^(?P<pk>\d+)/$',
                   view_class.as_view(**kwargs),
                   name='detail')
        return super(DetailMixin, self).collect_urls(item, *other)

    def build_detail_view(self):
        kwargs, view_class = self.wrap_view(generic_views.DetailView)
        kwargs.update({
            'template_name': self.detail_template_name,
            'model': self.model,
            'queryset': self.queryset,
        })
        return kwargs, view_class


class CreateMixin(viewsets.BaseViewSet):
    model = None
    queryset = None
    create_template_name = None
    initial = {}
    form_class = None
    fields = None
    create_success_url = None
    prefix = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_create_view()
        item = url('^add/$',
                   view_class.as_view(**kwargs),
                   name='add')
        return super(CreateMixin, self).collect_urls(item, *other)

    def build_create_view(self):
        kwargs, view_class = self.wrap_view(generic_views.CreateView)
        kwargs.update({
            'template_name': self.create_template_name,
            'model': self.model,
            'queryset': self.queryset,
            'form_class': self.form_class,
            'fields': self.fields,
            'success_url': self.create_success_url,
            'prefix': self.prefix,
        })
        return kwargs, view_class


class UpdateMixin(viewsets.BaseViewSet):
    model = None
    queryset = None
    update_template_name = None
    initial = {}
    form_class = None
    fields = None
    update_success_url = None
    prefix = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_update_view()
        item = url('^(?P<pk>\d+)/edit/$',
                   view_class.as_view(**kwargs),
                   name='edit')
        return super(UpdateMixin, self).collect_urls(item, *other)

    def build_update_view(self):
        kwargs, view_class = self.wrap_view(generic_views.UpdateView)
        kwargs.update({
            'template_name': self.update_template_name,
            'model': self.model,
            'queryset': self.queryset,
            'form_class': self.form_class,
            'fields': self.fields,
            'success_url': self.update_success_url,
            'prefix': self.prefix,
        })
        return kwargs, view_class


class DeleteMixin(viewsets.BaseViewSet):
    model = None
    queryset = None
    delete_template_name = None
    delete_success_url = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_delete_view()
        item = url('^(?P<pk>\d+)/delete/$',
                   view_class.as_view(**kwargs),
                   name='delete')
        return super(DeleteMixin, self).collect_urls(item, *other)

    def build_delete_view(self):
        kwargs, view_class = self.wrap_view(generic_views.DeleteView)
        kwargs.update({
            'template_name': self.delete_template_name,
            'model': self.model,
            'queryset': self.queryset,
            'success_url': self.delete_success_url,
        })
        return kwargs, view_class
