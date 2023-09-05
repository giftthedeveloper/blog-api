from django.shortcuts import render
from .views import BlogPostViewSet, BlogListViewSet, BlogCreateViewSet, BlogPostUpdateViewSet, \
    GrantEditPermissionView, SharedBlogViewSet, BlogPostWithPermissionsViewSet
from rest_framework import routers
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'', BlogPostViewSet, basename="blogs")
router.register(r'update', BlogPostUpdateViewSet, basename="blogs-update")
router.register(r'', BlogPostWithPermissionsViewSet, basename="blogs")

urlpatterns = [
    path('list',BlogListViewSet.as_view({'get': 'list'}), name='ordered-blog'),
    path('create',BlogCreateViewSet.as_view({'post': 'create'}), name='create-a-blog'),
    path('grant-edit-permission/', GrantEditPermissionView.as_view(), name='grant-edit-permission'),  
    path('shared-blogs/', SharedBlogViewSet.as_view({'get': 'list'}), name='shared-blogs'),    
  

]

urlpatterns += router.urls
