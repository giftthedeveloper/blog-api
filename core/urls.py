from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
# from app.urls import router_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="This is the Blog API Doc, An API, or Application Programming Interface, is a set of rules and protocols that enables different software applications to communicate and share data with each other.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="giftjeremiah001@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=(),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('app.urls')),

    re_path(
        r"^api/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
