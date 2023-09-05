from django.shortcuts import render
from .views import BlogPostViewSet, BlogListViewSet, BlogCreateViewSet, BlogPostUpdateViewSet
from rest_framework import routers
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename="blogs")
router.register(r'blog/update', BlogPostUpdateViewSet, basename="blogs")

urlpatterns = [
    path('blog/list',BlogListViewSet.as_view({'get': 'list'}), name='ordered-blog'),
    path('blog/create',BlogCreateViewSet.as_view({'post': 'create'}), name='create-a-blog'),
    # path('blog/update/<int:pk>',BlogPostUpdateViewSet.as_view({'patch': 'update'}), name='update-a-blog'),


]

urlpatterns += router.urls
