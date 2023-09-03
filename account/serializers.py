# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView



# class AdminUserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ["id", "username", "password", "email", "full_name", "role"]


# class UserSerializer(): 
#     class Meta(BaseUserSerializer.Meta):

#         fields = ["id", "email", "username", "date_joined",  "role", "is_active"]



# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['role'] = user.role  # assuming a "role" field on the user model
#         token['email'] = user.email
#         token['username'] = user.username
#         token['is_staff'] = user.is_staff
#         return token
