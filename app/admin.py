from django.contrib import admin
from .models import BlogPost, BlogPostPermission

@admin.register(BlogPost)
class BlogPost(admin.ModelAdmin):
    list_display = [field.name for field in BlogPost._meta.fields]

@admin.register(BlogPostPermission)
class BlogPostPermission(admin.ModelAdmin):
    list_display = [field.name for field in BlogPostPermission._meta.fields]