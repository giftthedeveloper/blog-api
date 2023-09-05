from rest_framework import serializers
from .models import Author
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "full_name", "bio"]
        
class AdminUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "full_name", "role", "is_staff", "is_superuser"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['username', 'email', 'full_name', 'profile_picture', 'bio']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role 
        token['email'] = user.email
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token
