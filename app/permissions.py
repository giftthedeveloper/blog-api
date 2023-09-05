from rest_framework import permissions
from .models import BlogPostPermission

# class IsAuthorPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # if  the user belongs to the authors group 
#         return request.user.groups.filter(name='author').exists()

from rest_framework import permissions

class CanEditBlogPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user has edit permission for the BlogPost
        if request.user == obj.author or BlogPostPermission.objects.filter(blog_post=obj, user=request.user, permission_type='edit').exists():
            return True
        return False

# class CanEditBlogPostPermission(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user == obj.author:
#             return True

#         if BlogPostPermission.objects.filter(blog_post=obj, user=request.user, permission_type='edit').exists():
#             return True

#         return False