from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegistrationSerializer, UserUpdateSerializer


class DeleteTokenApi(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Token, user = self.request.user)


class RegistrationUser(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class RetriveUpdateUser(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
