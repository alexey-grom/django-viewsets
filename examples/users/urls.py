# encoding: utf-8

from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from viewsets import generic, permissions


class UserViewset(generic.ModelViewSet):
    model = get_user_model()
    permission_check_classes = (permissions.ModelPermissionChecker, )


class GroupViewset(generic.ModelViewSet):
    model = Group


class PermissionViewset(generic.ModelViewSet):
    model = Permission


urlpatterns = [url('^users/', UserViewset().urls),
               url('^groups/', GroupViewset().urls),
               url('^permissions/', PermissionViewset().urls), ]
