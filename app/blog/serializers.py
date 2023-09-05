from rest_framework import serializers
from .models import BlogPost
from ..blog_permissions.serializers import BlogPostPermissionSerializer

class BlogPostSerializer(serializers.ModelSerializer):
    # permissions = BlogPostPermissionSerializer(many=True, read_only=True)
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'author', 'featured_image', 'content', 'slug', 
                  'created_at', 'updated_at', 'author_details')
        read_only_fields = ['slug']  

   
