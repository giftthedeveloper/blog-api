
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     role = serializers.CharField(default='author', read_only=True) 
#     class Meta:
#         model = User
#         fields = ['id', 'password', 'username', 'email', 'full_name', 'profile_picture', 'bio', 'date_of_birth', 'role', 'date_joined'
# ]

#         extra_kwargs = {
#             'password': {'write_only': True},  
#             'role': {'read_only': True},
#             # 'id': {'read_only': True},  
#         }

#     #enables passsword hashing
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         user = super().create(validated_data)
#         user.set_password(password)
#         user.role = "author"
#         user.save()
#         return user
        

class UserCreateSerializer(BaseUserCreateSerializer):
    full_name = serializers.ImageField(required=False) 
    bio = serializers.ImageField(required=False)
    # role = serializers.ImageField(required=False) 

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'password', 'username', 'email', 'full_name', 'bio',  'date_joined']

class UserSerializer(BaseUserSerializer): 
    full_name = serializers.ImageField(required=False) 
    bio = serializers.ImageField(required=False)
    role = serializers.ImageField(required=False) 


    class Meta(BaseUserSerializer.Meta):

        fields = ['id', 'password', 'username', 'email', 'full_name', 'bio', 'role', 'date_joined']

      
#for seperation of concerns and clarity of roles ensuring that only admins can create admins
class AdminSerializer(serializers.ModelSerializer): 
    role = serializers.CharField(default='admin', read_only=True)  # Set default and read-only
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
                'password': {'write_only': True},  # Ensure password is not included in response
                'id': {'read_only': True},  
            }
    #for password hashing
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.role = "admin"
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role  
        token['email'] = user.email
        token['username'] = user.username
        return token

