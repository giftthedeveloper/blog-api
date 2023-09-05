from django.urls import path

from rest_framework_simplejwt import views as simple_jwt_views
from .views import UserViewSet, AdminViewSet, LoginViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
router = DefaultRouter()


urlpatterns= [
    # path("auth/login/", LoginViewSet.as_view(), name="login"),  
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path('auth/signup/', UserViewSet.as_view(), name='user-signup'),
    # path('auth/<int:pk>/update-details/', UserViewSet.as_view({'patch': 'partial_update', 'put': 'update'}), name='user-update-details'),
    # path('auth/<int:pk>/delete-account/', UserViewSet.as_view({'delete': 'destroy'}), name='user-delete-account'),

    #seperation of concerns for admin. Admins may refer to owner of blog and developers in charge of maintaing the blog
    path('auth-admin/signup/', AdminViewSet.as_view({'post': 'create'}), name='admin-signup'),
    path('auth-admin/login/', LoginViewSet.as_view(), name='register-admin'),
    path('auth-admin/<int:pk>/update-details/', AdminViewSet.as_view({'patch': 'partial_update', 'put': 'update'}), name='user-update-details'),
    path('auth-admin/<int:pk>/delete-account/', AdminViewSet.as_view({'delete': 'destroy'}), name='user-delete-account'),


    # path("auth/password-reset/", UserViewSet.as_view({"post": "reset_password_confirm"}), name="confirm-password-reset")
]
