from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import (DeleteTokenApi, )


app_name = 'auth'
urlpatterns = [
    path('login/token-authenticate/', ObtainAuthToken.as_view(), name = 'login-token'),
    path('logout/token-authenticate/', DeleteTokenApi.as_view(), name = 'logout-token'),

]