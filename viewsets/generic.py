# encoding: utf-8

from viewsets import viewset
from viewsets import mixins


class BaseModelViewSet(mixins.PermissionsMixin,
                       mixins.ModelNamespaceMixin,
                       viewset.BaseViewSet):
    """"""


class ModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                   mixins.CreateMixin, mixins.UpdateMixin,
                   mixins.DeleteMixin,
                   BaseModelViewSet):
    """"""


class ReadOnlyModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                           BaseModelViewSet):
    """"""
