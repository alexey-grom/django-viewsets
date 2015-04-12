# encoding: utf-8

from viewsets import viewset
from viewsets import mixins


class BaseModelViewSet(mixins.GuardMixin, mixins.ModelNamespaceMixin, viewset.BaseViewSet):
    model = None

    @property
    def model_options(self):
        return self.model._meta


class ModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                   mixins.CreateMixin, mixins.UpdateMixin,
                   mixins.DeleteMixin,
                   BaseModelViewSet):
    """"""


class ReadOnlyModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                           BaseModelViewSet):
    """"""
