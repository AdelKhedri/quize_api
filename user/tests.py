# from datetime import timedelta
# from time import sleep
# from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
import json


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


class TestSignupApi(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData
        cls.login_url = reverse('auth:login-token')
        cls.url = reverse('auth:user-registration')
        cls.user_data = {
            'username': 'user1',
            'password': 'password',
            'password1': 'password',
            'password2': 'password',
            'first_name': 'parham',
            'last_name': 'testi'
        }
        cls.client = APIClient

    def test_registration_success(self):
        res = self.client.post(self.url, self.user_data)
        self.assertEqual(res.status_code, 201)
        res2 = self.client.post(self.login_url, self.user_data)
        token = json.loads(res2.content.decode('utf-8'))['token']
        self.assertTrue(len(token) > 20)

    def test_registration_error_unique_username(self):
        User.objects.create_user(username='user1', password='p')
        res = self.client.post(self.url, self.user_data)
        self.assertEqual(res.status_code, 400)

    def test_registration_password_required(self):
        del self.user_data['password1']
        del self.user_data['password2']
        res = self.client.post(self.url, {})
        password1 = json.loads(res.content)['password1']
        password2 = json.loads(res.content)['password2']
        self.assertEqual(res.status_code, 400)
        self.assertEqual(password1[0], 'This field is required.')
        self.assertEqual(password2[0], 'This field is required.')

    def test_registration_error_passwrod_not_match(self):
        self.user_data['password1'] = 'test'
        res = self.client.post(self.url, self.user_data)
        errors = json.loads(res.content)['non_field_errors']
        self.assertIn('passwords not match.', errors)


class TestUserUpdateApi(DRFTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.login_url = reverse('auth:login-token')
        cls.url = reverse('auth:user-update')

    def setUp(self):
        res = self.client.post(self.login_url, self.user_data)
        self.token = json.loads(res.content)['token']

    def test_update_username_success(self):
        updated_user_data = self.user_data
        updated_user_data['username'] = 'new_username'
        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(res.wsgi_request.user.username, updated_user_data['username'])

    def test_update_username_error_unique(self):
        User.objects.create_user(username='user2', password='password')
        updated_user_data = self.user_data
        updated_user_data['username'] = 'user2'

        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION=f'Token {self.token}')
        username = json.loads(res.content)['username']
        self.assertEqual(res.status_code, 400)
        self.assertEqual(username[0], 'A user with that username already exists.')

    def test_change_password_success(self):
        updated_user_data = self.user_data
        updated_user_data.update({
            'old_password': 'password',
            'password1': 'new_password',
            'password2': 'new_password',
            'password': 'new_password'
            })

        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(res.status_code, 200)
        res = self.client.post(self.login_url, updated_user_data)
        self.assertEqual(res.status_code, 200)

    def test_change_password_error_required_password1(self):
        updated_user_data = self.user_data
        updated_user_data['password2'] = 'password'

        res = self.client.put(self.url, self.user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        error = json.loads(res.content.decode('utf-8'))['password1']
        self.assertEqual(error[0], 'required')

    def test_change_password_error_required_password2(self):
        updated_user_data = self.user_data
        updated_user_data['password1'] = 'password'

        res = self.client.put(self.url, self.user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        error = json.loads(res.content.decode('utf-8'))['password2']
        self.assertEqual(error[0], 'required')

    def test_change_password_error_required_old_password(self):
        updated_user_data = self.user_data
        updated_user_data.update({
            'password1': 'password',
            'password2': 'password',
        })

        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        error = json.loads(res.content.decode('utf-8'))['old_password']
        self.assertEqual(error[0], 'required')

    def test_change_password_error_password_not_match(self):
        updated_user_data = self.user_data
        updated_user_data.update({
            'old_password': 'ss',
            'password1': 'password',
            'password2': 'password2',
        })

        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        error = json.loads(res.content.decode('utf-8'))['non_field_errors']
        self.assertEqual(error[0], 'passwords not match.')

    def test_change_password_error_odl_password_warring(self):
        updated_user_data = self.user_data
        updated_user_data.update({
            'old_password': 'ss',
            'password1': 'password',
            'password2': 'password',
        })

        res = self.client.put(self.url, updated_user_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        error = json.loads(res.content.decode('utf-8'))['old_password']
        self.assertEqual(error[0], 'old password is warring.')
