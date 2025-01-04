# from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
import json
from rest_framework.authtoken.models import Token


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

        cls.login = reverse('auth:login-token')
        cls.logout = reverse('auth:logout-token')
        cls.res = cls.client.post(cls.login, cls.user_data)
        token = json.loads(cls.res.content.decode('utf-8'))['token']
        cls.client.credentials(HTTP_AUTHORIZATION='Token ' + token) # failed. can not set header
    
    # def test_logout_success(self):
    #     self.client.force_login(user=self.user)
    #     res = self.client.post(self.logout)
    #     self.assertEqual(res.status_code, 204)