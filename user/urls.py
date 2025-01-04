from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import (DeleteTokenApi, )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'auth'
urlpatterns = [
    path('login/token-authenticate/', ObtainAuthToken.as_view(), name = 'login-token'),
    path('logout/token-authenticate/', DeleteTokenApi.as_view(), name = 'logout-token'),
    path('login/jwt/token/', TokenObtainPairView.as_view(), name= 'login-jwt'),
    path('login/jwt/token/refresh/', TokenRefreshView.as_view(), name= 'login-jwt-refresh'),
    path('login/jwt/token/check', TokenVerifyView.as_view(), name= 'login-jwt-check'),
]
