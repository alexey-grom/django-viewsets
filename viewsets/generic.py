# encoding: utf-8

from viewsets import viewset
from viewsets import mixins


class ModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                   mixins.CreateMixin, mixins.UpdateMixin,
                   mixins.DeleteMixin,
                   mixins.ModelNamespaceMixin, viewset.BaseViewSet):
    """"""


class ReadOnlyModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                           mixins.ModelNamespaceMixin, viewset.BaseViewSet):
    """"""
