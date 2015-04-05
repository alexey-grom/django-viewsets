# encoding: utf-8

from . import viewsets
from . import mixins


class ModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                   mixins.CreateMixin, mixins.UpdateMixin,
                   mixins.DeleteMixin,
                   mixins.ModelNamespaceMixin, viewsets.BaseViewSet):
    pass


class ReadOnlyModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                           mixins.ModelNamespaceMixin, viewsets.BaseViewSet):
    pass
