from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer,UserSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="User Registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "email", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
            example={
                "username": "mario",
                "email": "mario@example.com",
                "password": "Password123!"
            },
        ),
        responses={201: UserSerializer},
        tags=["Auth"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # restituisco i dati dell'utente creato senza password
            user = User.objects.get(username=request.data.get("username"))
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return response

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary="My Info",
        responses={200: UserSerializer},
        tags=["Auth"],
        security=[{"Bearer": []}],   
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

