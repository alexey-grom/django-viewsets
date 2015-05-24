# encoding: utf-8

from django.contrib.auth import get_permission_codename


class BasePermissionChecker(object):
    def __init__(self, viewset, viewname, request):
        self.viewset = viewset
        self.viewname = viewname
        self.request = request

    def has_view_access(self):
        """
        View level access checking
        """
        return True

    def has_object_access(self, obj):
        """
        Object level access checking
        """
        return True


class ModelPermissionChecker(BasePermissionChecker):
    permissions_map = {
        'list': lambda self: True,
        'detail': lambda self: True,
        'add': lambda self: self._has_auth_permission('add'),
        'edit': lambda self: self._has_auth_permission('change'),
        'delete': lambda self: self._has_auth_permission('delete'),
    }

    def has_view_access(self):
        checker = self.permissions_map.get(self.viewname,
                                           lambda _: True)
        return super(ModelPermissionChecker, self).has_view_access() and \
               checker(self)

    def has_object_access(self, obj):
        return self.has_view_access()

    def _has_auth_permission(self, name):
        codename = get_permission_codename(name, self.viewset.model_options)
        perm = '{}.{}'.format(self.viewset.model_options.app_label, codename)
        print self.request.user, perm, self.request.user.has_perm(perm)
        return self.request.user.has_perm(perm)


class LoginRequiredChecker(BasePermissionChecker):
    def has_view_access(self):
        is_authenticated = self.request.user and \
                           self.request.user.is_authenticated()
        return super(LoginRequiredChecker, self).has_view_access() and \
               is_authenticated

    def has_object_access(self, obj):
        return self.has_view_access()


class SuperuserRequiredChecker(LoginRequiredChecker):
    def has_view_access(self):
        is_superuser = self.request.user and \
                       self.request.user.is_authenticated() and \
                       self.request.user.is_superuser
        return super(SuperuserRequiredChecker, self).has_view_access() and \
               is_superuser

    def has_object_access(self, obj):
        return self.has_view_access()


class StaffRequiredChecker(LoginRequiredChecker):
    def has_view_access(self):
        is_staff = self.request.user and \
                   self.request.user.is_authenticated() and \
                   self.request.user.is_staff
        return super(StaffRequiredChecker, self).has_view_access() and \
               is_staff

    def has_object_access(self, obj):
        return self.has_view_access()
