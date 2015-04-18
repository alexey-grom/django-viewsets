Django Viewsets
===============

DRY app provides configurable groups of class-based views. 

Useful replacement of `django.contrib.admin`. It can also be used for fast build a CRUD interface.

Quick start
-----------

1. Install

    pip install git+https://github.com/alexey-grom/django-viewsets
    
2. Create viewset

    ```
    from viewsets.generic import ModelViewSet
    from viewsets.mixins import PermissionsMixin

    class PostViewSet(PermissionsMixin, ModelViewSet):
        model = models.Post
    ```

3. Add viewset to `urls.py`
    
    ```
    urlpatterns = [
        url(r'^posts/', PostViewSet().urls),
    ]
    ```

Generic viewsets
----------------

* `ModelViewSet`

    ```    
    /posts/             post:list                
    /posts/<pk>/        post:detail              
    /posts/<pk>/delete/ post:delete              
    /posts/<pk>/edit/   post:edit     
    /posts/add/         post:add     
    ```

* `ReadOnlyModelViewSet`

    ```
    /posts/             post:list
    /posts/<pk>/        post:detail
    ```

Generic mixins
--------------

* *Generic*

    * `ListMixin`
    * `DetailMixin` 
    * `CreateMixin` 
    * `UpdateMixin` 
    * `DeleteMixin` 

* *Permissions*

    * `GuardMixin`
    * `PermissionsMixin`

* *Namespaces*

    * `NamespaceMixin`
    * `ModelNamespaceMixin`
