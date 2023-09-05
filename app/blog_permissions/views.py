
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPostPermission
from ..permissions import CanEditBlogPostPermission
from .serializers import GrantEditPermissionSerializer
from account.models import User
from .models import BlogPost  # Import the BlogPost model

class GrantEditPermissionView(generics.CreateAPIView):
    serializer_class = GrantEditPermissionSerializer
    permission_classes = [CanEditBlogPostPermission]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        blog_post = BlogPost.objects.get(pk=self.kwargs['pk'])  

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with the specified email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking to see if the user attempting to grant the permission is the owner of the blogpost
        if blog_post.author == request.user:
            # if the grantee already has permissions
            if BlogPostPermission.objects.filter(blog_post=blog_post, user=user, permission_type='edit').exists():
                return Response({"error": "Permission already granted for this user."}, status=status.HTTP_400_BAD_REQUEST)

            
            BlogPostPermission.objects.create(blog_post=blog_post, user=user, permission_type='edit')
            return Response({"message": "Edit permission granted successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Permission denied. You are not the owner of this blog post."}, status=status.HTTP_403_FORBIDDEN)