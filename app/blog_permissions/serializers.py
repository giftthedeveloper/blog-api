from ..blog.models import BlogPost
from rest_framework import serializers
from .models import BlogPostPermission
from account.models import Author

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

# class BlogPostPermissionSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = BlogPostPermission
#         fields = ('user',)

#     def get_user(self, obj):
#         return obj.user.author_details  


class BlogPostPermissionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    blog_post = SharedBlogSerializer(many=True, read_only=True)
    class Meta:
        model = BlogPostPermission
        fields = ('user', 'blog_post')

    def get_user(self, obj):
        return obj.user.author_details  