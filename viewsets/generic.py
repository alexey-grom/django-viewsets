# encoding: utf-8

from . import viewsets
from . import mixins
from . import helpers


class ModelNamespaceMixin(viewsets.BaseViewSet):
    model = None

    def get_namespace(self):
        namespace = super(ModelNamespaceMixin, self).get_namespace()
        if namespace is None and self.model:
            namespace = helpers.camelcase_to_dash(self.model.__name__)
        return namespace



class ModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                   mixins.CreateMixin, mixins.UpdateMixin,
                   mixins.DeleteMixin,
                   ModelNamespaceMixin, viewsets.BaseViewSet):
    pass


class ReadOnlyModelViewSet(mixins.ListMixin, mixins.DetailMixin,
                           ModelNamespaceMixin, viewsets.BaseViewSet):
    pass
