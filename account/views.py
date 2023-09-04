from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer, LoginSerializer
from rest_framework import viewsets, status, generics
from .models import User
from .serializers import UserSerializer, AdminSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from .permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import authenticate, login


#viewset to enable authors  create, update details and delete account
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [FormParser, MultiPartParser]

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        print("this" + password)
        serializer.save(password=self.request.data.get('password'))
 
#sepration of concerns in roles. to ensure only admins can create an admin and view admin stuffs. Regular users(authors) cannot
class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes  = [IsAdminUser]

class LoginViewSet(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            if not user.is_active:
                return Response({'message': 'Account not activated'}, status=status.HTTP_403_FORBIDDEN)

            login(request, user)

            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            return Response({
                'message': 'Logged in successfully',
                'refresh_token': str(refresh_token),
                'access_token': str(access_token)},
              status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
