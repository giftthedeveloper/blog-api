
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from .models import BlogPostPermission
from .serializers import GrantEditPermissionSerializer, SharedBlogSerializer, \
    BlogPostPermissionSerializer
from account.models import Author
from .models import BlogPost  
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions, decorators
from django.db.models import Q
from ..blog.serializers import BlogPostSerializer

action = decorators.action
class GrantEditPermissionView(generics.CreateAPIView):
    serializer_class = GrantEditPermissionSerializer
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('blog_id', openapi.IN_QUERY, description="Enter the blog id to grant permission", type=openapi.TYPE_INTEGER),
        ],
        operation_description="Grant another author edit permission",
        responses={200: GrantEditPermissionSerializer(many=True)},
    )

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        # blog_id = request.query_params.get('blog_id') 
        blog_id = request.data.get('blog_id') 

        
        try:
            blog_post = BlogPost.objects.get(pk=blog_id) 
        except BlogPost.DoesNotExist:
            return Response({"error": "BlogPost with the specified id does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Author.objects.get(email=email)
        except Author.DoesNotExist:
            return Response({"error": "User with the specified email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking to see if the user attempting to grant the permission is the owner of the blogpost
        if blog_post.author == request.user:
            # if the grantee already has permissions
            if BlogPostPermission.objects.filter(blog_post=blog_post, user=user, permission_type='edit').exists():
                return Response({"error": "Permission already granted for this user."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                BlogPostPermission.objects.create(blog_post=blog_post, user=user, permission_type='edit')
            return Response({"message": "Edit permission granted successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Permission denied for Unauthorized user. You are not the owner of this blog post."}, status=status.HTTP_403_FORBIDDEN)


#class to return list of blogs the user has access to
class SharedBlogViewSet(viewsets.GenericViewSet):
    serializer_class = SharedBlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  
        if user.is_authenticated:
            # Filter the blog posts where the user has edit access or is the owner
            queryset = BlogPost.objects.filter(
                Q(author=user) | Q(blogpostpermission__user=user, blogpostpermission__permission_type='edit')
            ).distinct()
        else:
            queryset = BlogPost.objects.none() 
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogPostWithPermissionsViewSet(viewsets.GenericViewSet):
    queryset = BlogPostPermission.objects.all()
    serializer_class = BlogPostPermissionSerializer

    @action(detail=True, methods=['GET'])
    def blog_authors_list(self, request, pk=None):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        permissions = BlogPostPermission.objects.filter(blog_post=blog_post, permission_type__in=['edit', 'view'])

        authors_with_access = []
        for permission in permissions:
            author = permission.user
            author_details = {
                "id": author.id,
                "profile_image": author.profile_picture.url if author.profile_picture else None,
                "username": author.username,
            }
            authors_with_access.append(author_details)

        data = {
            "blog_id": blog_post.id,
            "blog_title": blog_post.title,
            "blog_author": blog_post.author_details,
            "authors_with_access": authors_with_access,
        }
        return Response(data)
