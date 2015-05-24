# encoding: utf-8

from collections import OrderedDict

from django.conf.urls import url, patterns, include
from django.core.exceptions import PermissionDenied
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField, ForeignKey, ManyToManyField

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

    @property
    def read_write_fields(self):
        return self.get_read_write_fields()

    def get_read_write_fields(self):
        return [
            field.name
            for field in self.model_options.get_fields(include_parents=False)
            if isinstance(field, Field)
        ]


class ModelNamespaceMixin(NamespaceMixin, ModelMixin):
    def get_namespace(self):
        if not hasattr(self, '_namespace'):
            namespace = super(ModelNamespaceMixin, self).get_namespace()
            if namespace is None and self.model:
                namespace = helpers.camelcase_to_dash(self.model.__name__)
            self._namespace = namespace
        return self._namespace


class ModelSerializeMixin(ModelMixin, viewset.BaseViewSet):
    def serialize_object(self, obj):
        fields = []

        for field in self.model_options.get_fields(include_parents=False):
            result = self.serialize_field(field, obj)
            if not result:
                continue
            fields.append(result)

        return OrderedDict(fields)

    def serialize_field(self, field, obj):
        if not isinstance(field, Field):
            return

        title = field.verbose_name
        value = getattr(obj, field.name)

        if isinstance(field, ForeignKey):
            value = unicode(value)

        elif isinstance(field, ManyToManyField):
            value = unicode(value.all()[:3])

        else:
            pass

        return title, value


class GuardMixin(viewset.BaseViewSet):
    def pre_dispatch_request(self, view, request):
        """
        View level access checking
        """

    def check_object(self, view, request, obj):
        """
        Object level access checking
        """

    def get_mixin_classes(self, view_class):
        mixin_classes = (views.DispatchViewMixin, ) + super(GuardMixin, self).get_mixin_classes(view_class)
        if issubclass(view_class, views.SingleObjectMixin):
            mixin_classes = mixin_classes + (views.CheckObjectViewMixin, )
        return mixin_classes


class PermissionsMixin(GuardMixin, ModelMixin):
    model = None
    permission_check_classes = ()

    # GuardMixin behaviour methods

    def pre_dispatch_request(self, view, request):
        super(PermissionsMixin, self).pre_dispatch_request(view, request)
        if not self.has_view_access(view.view_name, request):
            self.raise_forbidden(request, view)

    def check_object(self, view, request, obj):
        super(PermissionsMixin, self).check_object(view, request, obj)
        if not self.has_object_access(view.view_name, request, obj):
            self.raise_forbidden(request, view, obj)

    # permission denied behaviour

    def raise_forbidden(self, view, request, obj=None):
        raise PermissionDenied()

    # permission checkers call

    def has_view_access(self, viewname, request):
        for checker_class in self.permission_check_classes:
            if not checker_class(self, viewname, request).has_view_access():
                return False
        return True

    def has_object_access(self, viewname, request, obj):
        for checker_class in self.permission_check_classes:
            if not checker_class(self, viewname, request).has_object_access(obj):
                return False
        return True

    def has_access(self, viewname, request, obj=None):
        """Proxy-method for `has_view_access` and `has_object_access` depends on `obj`"""
        if obj:
            return self.has_object_access(viewname, request, obj)
        return self.has_view_access(viewname, request)


class ListMixin(ModelSerializeMixin):
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


class DetailMixin(ModelSerializeMixin):
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
            'fields': self.fields or self.read_write_fields,
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
            'fields': self.fields or self.read_write_fields,
            'prefix': self.prefix,
        }


class DeleteMixin(ModelSerializeMixin):
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
