
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from .models import BlogPostPermission
from .serializers import GrantEditPermissionSerializer, SharedBlogSerializer
from account.models import Author
from .models import BlogPost  
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions


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

#class to return list of blogs for a user alomgside with autheor acess information

class SharedBlogViewSet(viewsets.GenericViewSet):
    serializer_class = SharedBlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    # List shared blogs with their details and authors with edit access
    def list(self, request, *args, **kwargs):
        user = self.request.user

        try:
            shared_blog_ids = BlogPostPermission.objects.filter(user=user, permission_type='edit').values_list('blog_post__id', flat=True)
            shared_blogs = BlogPost.objects.filter(id__in=shared_blog_ids)
            shared_blogs_data = self.get_serializer(shared_blogs, many=True).data

            # Getting authors with edit access to shared blogs
            authors_with_access = BlogPostPermission.objects.filter(blog_post__in=shared_blog_ids, permission_type='edit').values_list('user__id', flat=True)
            author_details = {
                author.id: author.author_details for author in Author.objects.filter(id__in=authors_with_access)
            }

            # Add author details to shared blog data
            for blog_data in shared_blogs_data:
                blog_id = blog_data['id']
                if blog_id in author_details:
                    blog_data['authors_with_access'] = author_details[blog_id]
                else:
                    blog_data['authors_with_access'] = []

            return Response(shared_blogs_data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
