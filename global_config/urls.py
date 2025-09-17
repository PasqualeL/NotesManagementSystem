from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .utils import root_redirect, logout_get 
from iam.views import RegisterUserView, CurrentUserView
from notes_management_system.views import NoteViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

# SWAGGER Region
schema_view = get_schema_view(
    openapi.Info(
        title="Notes Management API",
        default_version="v1",
        description=("Authentication: user registration, login to obtain the token and call the APIs via Postman using JWT bearer token authentication\n\n"  
                    "Note section:\n"
                    "CRUD APIs and a list of the user’s notes with filtering and search."
        )
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

# IAM api
iam_url = [
    path("iam/auth/register/", RegisterUserView.as_view(), name="register"),
    path("iam/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("iam/auth/currentuser/", CurrentUserView.as_view(), name="current_user"),
]

# Swagger url
swagger_url = [
    path("swagger/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("swagger/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

urlpatterns = [
    path("", root_redirect, name="root"),
    path('admin/', admin.site.urls),
    path("api/auth/session/logout/", logout_get, name="session-logout"),
    path("api/auth/session/", include("rest_framework.urls")),
    path('api/', include(router.urls)),
] + iam_url + swagger_url
