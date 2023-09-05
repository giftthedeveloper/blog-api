from django.shortcuts import render
from .views import BlogPostViewSet, BlogListViewSet, BlogCreateViewSet, BlogPostUpdateViewSet
from rest_framework import routers
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename="blogs-by-id")
# router.register(r'blog/create', BlogCreateViewSet, basename="blog-create")

urlpatterns = [
    path('blog/list',BlogListViewSet.as_view({'get': 'list'}), name='ordered-blog'),
    path('blog/create', BlogCreateViewSet.as_view({ 'post': 'create'}), name="blog-create"),
    path('blog/update', BlogPostUpdateViewSet.as_view({ 'put': 'update', 'patch': 'update'}), name="blog-create")

]

urlpatterns += router.urls
