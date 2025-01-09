import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import TestQuestion


class TestListCreateTestQuestionAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='password')
        cls.token = Token.objects.create(user=user).key
        cls.url = reverse('quize:test-question-list-create')
        cls.question_data = {
            'text_question': 'Question1',
            'choise1': 'test1',
            'choise2': 'test2',
            'choise3': 'test3',
            'choise4': 'test4',
            'correct_choise': 1,
            'point': 2.5,
            'creator_id': 1
        }
        question_list = []
        for i in range(53):
            question_list.append(TestQuestion(**cls.question_data))
        TestQuestion.objects.bulk_create(question_list)

    def test_permission_authentication_needed(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 401)

    def test_permission_is_creator_needed(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(len(json.loads(res.content)['results']), 50)

    def test_pagination(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        total_question = data['count']
        next_page = data['next']
        self.assertEqual(total_question, 53)
        self.assertEqual(next_page, 'http://testserver/quize/test/question/list-create/?page=2')
        res = self.client.get(self.url + '?page=2', HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        last_page = data['previous']
        self.assertEqual(last_page, 'http://testserver/quize/test/question/list-create/')
        self.assertEqual(len(data['results']), 3)

    def test_create_question_success(self):
        res = self.client.post(self.url, self.question_data, HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['text_question'], self.question_data['text_question'])

    def test_create_question_required_fields(self):
        res = self.client.post(self.url, HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        fields = ['text_question', 'choise1', 'choise2', 'choise3', 'choise3', 'choise4', 'correct_choise', 'point']
        for field in fields:
            with self.subTest(field=field):
                self.assertEqual(data[field][0], 'This field is required.')


class TestRetriveUpdateTestQuestionAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='password')

        cls.question_data = {
            'text_question': 'text',
            'choise1': 'test1',
            'choise2': 'test2',
            'choise3': 'test3',
            'choise4': 'test4',
            'correct_choise': 1,
            'creator': user,
            'point': 1.75
        }

        cls.token = Token.objects.create(user=user).key
        cls.url = reverse('quize:test-question-retrive-update', kwargs={'pk': 1})

    def test_update_success(self):
        updated_question_data = self.question_data
        updated_question_data['name'] = 'new question'
        res = self.client.put(self.url, updated_question_data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content)['text_question'], updated_question_data['text_question'])

    def test_retrive_question(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(json.loads(res.content)['text_question'], self.question_data['text_question'])