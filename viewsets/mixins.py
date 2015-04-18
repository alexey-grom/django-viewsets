# encoding: utf-8

from django.contrib.auth import get_permission_codename
from django.conf.urls import url, patterns, include
from django.core.exceptions import PermissionDenied

from viewsets import viewset
from viewsets import views
from viewsets import helpers


class NamespaceMixin(viewset.BaseViewSet):
    namespace = None

    def get_namespace(self):
        return self.namespace

    def get_urls(self):
        urls = self.collect_urls()
        nested = patterns('', *urls)
        return include(nested, namespace=self.get_namespace())

    def reverse(self, name, *args, **kwargs):
        name = '{}:{}'.format(self.get_namespace(), name)
        return super(NamespaceMixin, self).reverse(name, *args, **kwargs)


class ModelMixin(viewset.BaseViewSet):
    model = None

    @property
    def model_options(self):
        return self.model._meta


class ModelNamespaceMixin(NamespaceMixin, ModelMixin):
    def get_namespace(self):
        if not hasattr(self, '_namespace'):
            namespace = super(ModelNamespaceMixin, self).get_namespace()
            if namespace is None and self.model:
                namespace = helpers.camelcase_to_dash(self.model.__name__)
            self._namespace = namespace
        return self._namespace


class GuardMixin(viewset.BaseViewSet):
    def pre_dispatch_request(self, view, request):
        """
        table level permissions
        """

    def check_object(self, view, request, obj):
        """
        row level permissions
        """

    def get_mixin_classes(self, view_class):
        mixin_classes = (views.DispatchViewMixin, ) + super(GuardMixin, self).get_mixin_classes(view_class)
        if issubclass(view_class, views.SingleObjectMixin):
            mixin_classes = mixin_classes + (views.CheckObjectViewMixin, )
        return mixin_classes


class PermissionsMixin(GuardMixin, ModelMixin):
    model = None

    def pre_dispatch_request(self, view, request):
        super(PermissionsMixin, self).pre_dispatch_request(view, request)
        if not self.is_has_permission(request, view.view_name):
            self.raise_forbidden(request, view)

    def check_object(self, view, request, obj):
        super(PermissionsMixin, self).check_object(view, request, obj)
        if not self.is_has_permission(request, view.view_name, obj):
            self.raise_forbidden(request, view, obj)

    def raise_forbidden(self, view, request, obj=None):
        raise PermissionDenied()

    def is_has_permission(self, request, view_name, obj=None):
        if view_name == 'list':
            return True
        if view_name == 'detail':
            return True
        if view_name == 'add':
            return self.has_auth_permission(request, 'add')
        if view_name == 'edit':
            return self.has_auth_permission(request, 'change')
        if view_name == 'delete':
            return self.has_auth_permission(request, 'delete')
        return True

    def has_auth_permission(self, request, name):
        codename = get_permission_codename(name, self.model_options)
        perm = '{}.{}'.format(self.model_options.app_label, codename)
        return request.user.has_perm(perm)


class ListMixin(ModelMixin, viewset.BaseViewSet):
    queryset = None
    paginate_by = 100

    def collect_urls(self, *other):
        kwargs, view_class = self.build_list_view()
        item = url('^$', view_class.as_view(**kwargs), name='list')
        return super(ListMixin, self).collect_urls(item, *other)

    def build_list_view(self):
        kwargs, view_class = self.wrap_view(self.get_list_class())
        kwargs.update(self.get_list_kwargs())
        return kwargs, view_class

    def get_list_class(self):
        return views.ListView

    def get_list_kwargs(self):
        return {
            'model': self.model,
            'queryset': self.queryset,
            'paginate_by': self.paginate_by,
        }


class DetailMixin(ModelMixin, viewset.BaseViewSet):
    queryset = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_detail_view()
        item = url('^(?P<pk>\d+)/$', view_class.as_view(**kwargs), name='detail')
        return super(DetailMixin, self).collect_urls(item, *other)

    def build_detail_view(self):
        kwargs, view_class = self.wrap_view(self.get_detail_class())
        kwargs.update(self.get_detail_kwargs())
        return kwargs, view_class

    def get_detail_class(self):
        return views.DetailView

    def get_detail_kwargs(self):
        return {
            'model': self.model,
            'queryset': self.queryset,
        }


class CreateMixin(ModelMixin, viewset.BaseViewSet):
    queryset = None
    initial = {}
    form_class = None
    fields = None
    prefix = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_create_view()
        item = url('^add/$', view_class.as_view(**kwargs), name='add')
        return super(CreateMixin, self).collect_urls(item, *other)

    def build_create_view(self):
        kwargs, view_class = self.wrap_view(self.get_create_class())
        kwargs.update(self.get_create_kwargs())
        return kwargs, view_class

    def get_create_class(self):
        return views.CreateView

    def get_create_kwargs(self):
        return {
            'model': self.model,
            'queryset': self.queryset,
            'form_class': self.form_class,
            'fields': self.fields,
            'prefix': self.prefix,
        }


class UpdateMixin(ModelMixin, viewset.BaseViewSet):
    queryset = None
    initial = {}
    form_class = None
    fields = None
    prefix = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_update_view()
        item = url('^(?P<pk>\d+)/edit/$', view_class.as_view(**kwargs), name='edit')
        return super(UpdateMixin, self).collect_urls(item, *other)

    def build_update_view(self):
        kwargs, view_class = self.wrap_view(self.get_update_class())
        kwargs.update(self.get_update_kwargs())
        return kwargs, view_class

    def get_update_class(self):
        return views.UpdateView

    def get_update_kwargs(self):
        return {
            'model': self.model,
            'queryset': self.queryset,
            'form_class': self.form_class,
            'fields': self.fields,
            'prefix': self.prefix,
        }


class DeleteMixin(ModelMixin, viewset.BaseViewSet):
    queryset = None

    def collect_urls(self, *other):
        kwargs, view_class = self.build_delete_view()
        item = url('^(?P<pk>\d+)/delete/$', view_class.as_view(**kwargs), name='delete')
        return super(DeleteMixin, self).collect_urls(item, *other)

    def build_delete_view(self):
        kwargs, view_class = self.wrap_view(self.get_delete_class())
        kwargs.update(self.get_delete_kwargs())
        return kwargs, view_class

    def get_delete_class(self):
        return views.DeleteView

    def get_delete_kwargs(self):
        return {
            'model': self.model,
            'queryset': self.queryset,
        }
