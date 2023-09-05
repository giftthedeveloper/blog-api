from django.shortcuts import render
from .views import BlogPostViewSet, BlogListViewSet, BlogCreateViewSet, BlogPostUpdateViewSet, \
    GrantEditPermissionView, SharedBlogViewSet
from rest_framework import routers
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename="blogs")
router.register(r'blog/update', BlogPostUpdateViewSet, basename="blogs-update")
# router.register(r'blog/shared-blogs', SharedBlogViewSet, basename="shared-blogs")

urlpatterns = [
    path('blog/list',BlogListViewSet.as_view({'get': 'list'}), name='ordered-blog'),
    path('blog/create',BlogCreateViewSet.as_view({'post': 'create'}), name='create-a-blog'),
    path('blog/grant-edit-permission/', GrantEditPermissionView.as_view(), name='grant-edit-permission'),  
    path('blog/shared-blogs/', SharedBlogViewSet.as_view({'get': 'list'}), name='shared-blogs'),    
  
    #shared blog endpoint
    #give access to another user

]

urlpatterns += router.urls
