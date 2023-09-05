# from django.shortcuts import render
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import  UserSerializer, LoginSerializer
# from rest_framework import viewsets, status, generics
# from .models import User
# from .serializers import UserSerializer, AdminSerializer
# from rest_framework.parsers import FormParser, MultiPartParser
# from .permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# from django.contrib.auth import authenticate, login


# #viewset to enable authors  create, update details and delete account
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     parser_classes = [FormParser, MultiPartParser]

#     def perform_create(self, serializer):
#         password = self.request.data.get('password')
#         serializer.save(password=self.request.data.get('password'))
 
# #sepration of concerns in roles. to ensure only admins can create an admin and view admin stuffs. Regular users(authors) cannot
# class AdminViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = AdminSerializer
#     parser_classes = [FormParser, MultiPartParser]
#     # permission_classes  = [IsAdminUser]

#     def perform_create(self, serializer):
#         password = self.request.data.get('password')
#         print("this" + password)
#         serializer.save(password=self.request.data.get('password'))


# class LoginViewSet(generics.CreateAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         username = serializer.validated_data.get('username')
#         password = serializer.validated_data.get('password')

#         user = User.objects.filter(username=username).first()
#         if user is not None and user.check_password(password):
#             if not user.is_active:
#                 return Response({'message': 'Account not activated'}, status=status.HTTP_403_FORBIDDEN)

#             login(request, user)

#             access_token = AccessToken.for_user(user)
#             refresh_token = RefreshToken.for_user(user)

#             return Response({
#                 'message': 'Logged in successfully',
#                 'refresh_token': str(refresh_token),
#                 'access_token': str(access_token)},
#               status=status.HTTP_200_OK)

#         else:
#             return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

# # class MyTokenObtainPairView(TokenObtainPairView):
# #     serializer_class = MyTokenObtainPairSerializer


from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from os import path
from .models import User
from .serializers import AdminUserCreateSerializer, MyTokenObtainPairSerializer
# Create your views here.

class UserViewSet(DjoserUserViewSet):
	def perform_update(self, serializer):
		super().perform_update(serializer)

		

class AdminUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserCreateSerializer

    def post(self, request):
        data = {**request.data, "role": "admin"}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

