from django.shortcuts import render
from .views import BlogPostViewSet, BlogListViewSet
from rest_framework import routers
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename="blogs")

urlpatterns = [
    path('blog/list',BlogListViewSet.as_view({'get': 'list'}), name='ordered-blog')
]

urlpatterns += router.urls
