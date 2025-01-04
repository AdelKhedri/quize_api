from datetime import timedelta
from time import sleep
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
import json
from rest_framework.authtoken.models import Token
import requests


class DRFTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_data = {
            'username': 'user1',
            'password': 'password'
        }
        cls.user = User.objects.create_user(**cls.user_data)

        cls.client = APIClient()



class TestLoginWithToken(DRFTestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('auth:login-token')
    
    def test_login_success(self):
        res = self.client.post(self.url, self.user_data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.content)['token'])

    def test_login_unsuccess_none_field_error(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 400)
    
    def test_login_unsuccess_fake_user_password(self):
        res = self.client.post(self.url, {'username': 'user1', 'password': 'ss'})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content.decode('utf-8'))['non_field_errors'][0], 'Unable to log in with provided credentials.')
    

class TestLogoutWithToken(DRFTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.logout = reverse('auth:logout-token')
        res = cls.client.post(reverse('auth:login-token'), cls.user_data)
        cls.token = json.loads(res.content.decode('utf-8'))['token']
        # cls.client.credentials(HTTP_AUTHORIZATION='Token ' + cls.token) # failed. can not set header

    def test_logout_success(self):
        res = self.client.delete(self.logout, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(res.status_code, 204)

    def test_logout_failed_invalid_token(self):
        res = self.client.delete(self.logout, HTTP_AUTHORIZATION = f'Token {self.token}')
        res = self.client.delete(self.logout, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(json.loads(res.content.decode('utf-8'))['detail'], 'Invalid token.')





class TestLoginWithJWT(DRFTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.login_url = reverse('auth:login-jwt')
        cls.refresh_url = reverse('auth:login-jwt-refresh')
        cls.check_access_token = reverse('auth:login-jwt-check')

    def test_login_success(self):
        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.status_code, 200) 
        self.assertIn('access', json.loads(res.content.decode('utf-8')))
        self.assertIn('refresh', json.loads(res.content.decode('utf-8')))

    def test_login_failed_invalid_username_password(self):
        self.user_data.update({'username': 'test'})
        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(json.loads(res.content.decode('utf-8'))['detail'], 'No active account found with the given credentials')

    # @override_settings(SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME": timedelta(seconds=1), 'LEEWAY': timedelta(seconds=1)})
    # def test_login_failed_expire_access_token(self):
    #     res = self.client.post(self.login_url, self.user_data)
    #     loaded_data = json.loads(res.content)
    #     access_token = loaded_data['access']
    #     sleep(3)
    #     res2 = self.client.post(self.check_access_token, {'token': access_token})
    #     self.assertEqual(json.loads(res2.content), 's')

    def test_get_new_access_token(self):
        res = self.client.post(self.login_url, self.user_data)
        loaded_data = json.loads(res.content)
        access, refresh = loaded_data['access'], loaded_data['refresh']

        new_res = self.client.post(self.refresh_url, {'refresh': refresh})
        loaded_data = json.loads(new_res.content)
        new_access = loaded_data['access']

        self.assertIn('access', loaded_data)
        self.assertNotEqual(access, new_access)

