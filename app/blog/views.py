from rest_framework import generics, viewsets, status, response, mixins
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostUpdateSerializer
from ..permissions import CanEditBlogPost
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import Http404, HttpResponseForbidden

class CustomPagination(PageNumberPagination):
    #allows max number of 20 posts per page
    page_size = 20
    page_size_query_param = 'page_size'  
    max_page_size = 20

#class to create a blog 
class BlogCreateViewSet(viewsets.GenericViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class to get specific blogpost with pagination
class BlogPostViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['author__username', 'created_at', 'slug', 'title']

#class to get all orders with the option of search fields, sorting by field, desc or asc
class BlogListViewSet(viewsets.GenericViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = CustomPagination  
    filter_backends = [SearchFilter]
    search_fields = ['author__username', 'created_at', 'slug', 'title']
    ordering_fields = ['created_at', 'id', 'title', 'author__username', 'slug']

    #to customize swagger to display sort field, sort_order and search parameters
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('sort_field', openapi.IN_QUERY, description="Field to sort by", type=openapi.TYPE_STRING),
            openapi.Parameter('sort_order', openapi.IN_QUERY, description="Sort order (asc or desc)", type=openapi.TYPE_STRING, enum=['asc', 'desc']),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search parameter", type=openapi.TYPE_STRING),
        ],
        operation_description="Description of your list operation",
        responses={200: BlogPostSerializer(many=True)},
    )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        search_param = request.query_params.get('search')
        sort_field = request.query_params.get('sort_field')
        sort_order = request.query_params.get('sort_order', 'asc')

        # If only the search parameter is provided, filter the queryset based on it.
        if search_param:
            queryset = queryset.filter(
                Q(author__username__icontains=search_param) |
                Q(created_at__icontains=search_param) |
                Q(slug__icontains=search_param) |
                Q(title__icontains=search_param)
            )

        # Handle sorting based on the provided parameters
        if sort_field and sort_field in self.ordering_fields:
            if sort_order == 'asc':
                queryset = queryset.order_by(sort_field)
            elif sort_order == 'desc':
                queryset = queryset.order_by(f'-{sort_field}')
        elif sort_field:  # Handle invalid sort_field values
            return response.Response({'detail': 'Invalid sort_field'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)



class BlogPostUpdateViewSet(viewsets.GenericViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostUpdateSerializer
    permission_classes = [ CanEditBlogPost]
    parser_classes = [FormParser, MultiPartParser]

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response_data = {'detail': 'Unauthorized. You must be authenticated and also be an author with permission to this blog to perform this action.'}
            return response.Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid() :
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        # Filter queryset to only include objects that the user has permission to edit

        user = self.request.user
        if user.is_authenticated:
            return BlogPost.objects.filter(
                Q(author=user) | Q(blogpostpermission__user=user, blogpostpermission__permission_type='edit')
            ).distinct()
        else:
            return BlogPost.objects.none()  # Return an empty queryset for anonymous users
