from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BlogPost._meta.fields]
