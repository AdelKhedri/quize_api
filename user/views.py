from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated


class DeleteTokenApi(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Token, user = self.request.user)