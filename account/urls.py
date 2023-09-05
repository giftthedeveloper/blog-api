from django.urls import path
from rest_framework_simplejwt import views as simple_jwt_views
from .views import UserViewSet, AdminUserView, MyTokenObtainPairView, UserUpdateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
    
router.register(r'auth/update-author-details', UserUpdateViewSet, basename='update-user-details')

urlpatterns= [
    path("auth/login/", MyTokenObtainPairView.as_view(), name="login"),  
    path("auth/refresh/", simple_jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("auth/verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path('auth/signup/', UserViewSet.as_view({"post": "create"}), name='register-a-user'),
    path('auth/signup-admin/', AdminUserView.as_view(), name='register-admin'),
]

urlpatterns += router.urls