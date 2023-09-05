from ..blog.models import BlogPost
from rest_framework import serializers
from .models import BlogPostPermission

class BlogPostPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostPermission
        fields = '__all__'


class GrantEditPermissionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    blog_id = serializers.IntegerField()

class SharedBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'author_details']

    # def get_author_details(self, obj):
    #     return obj.author_details