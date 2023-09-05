from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework import status, viewsets
from os import path
from .models import Author
from .serializers import AdminUserCreateSerializer, MyTokenObtainPairSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser

#to create author users
class UserViewSet(DjoserUserViewSet):
	def perform_update(self, serializer):
          
		super().perform_update(serializer)

#to handle user update records          
class UserUpdateViewSet(viewsets.GenericViewSet, UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def perform_update(self, serializer):
        serializer.save()


#to create admins for blog owner control and developer testing
class AdminUserView(GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AdminUserCreateSerializer

    def post(self, request):
        data = {**request.data, "role": "admin"}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#generates token for login and access
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

