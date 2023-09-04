
from rest_framework import serializers
from .models import BlogPostPermission

class BlogPostPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostPermission
        fields = '__all__'


class GrantEditPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()

