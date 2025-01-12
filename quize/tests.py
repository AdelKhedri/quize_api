import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Category, TestQuestion, TestQuiz


class TestListCreateTestQuestionAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='password')
        cls.token = Token.objects.create(user=user).key
        cls.url = reverse('quiz:test-question-list-create')
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
        self.assertEqual(next_page, 'http://testserver/quiz/test/question/list-create/?page=2')
        res = self.client.get(self.url + '?page=2', HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        last_page = data['previous']
        self.assertEqual(last_page, 'http://testserver/quiz/test/question/list-create/')
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
        TestQuestion.objects.create(**cls.question_data)
        cls.token = Token.objects.create(user=user).key
        cls.url = reverse('quiz:test-question-retrive-update', kwargs={'pk': 1})

    def test_update_success(self):
        updated_question_data = self.question_data
        updated_question_data['name'] = 'new question'
        res = self.client.put(self.url, updated_question_data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content)['text_question'], updated_question_data['text_question'])

    def test_retrive_question(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(json.loads(res.content)['text_question'], self.question_data['text_question'])


class TestCategorysAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='password')
        cls.token = Token.objects.create(user=user).key
        cls.url = reverse('quiz:categorys-list')
        category_list = []

        for num in range(53):
            name = f'category{num}'
            allow_quiz_assignment = True if num%2 == 0 else False
            category_list.append(Category(name=name, slug=name, allow_quiz_assignment=allow_quiz_assignment))
        Category.objects.bulk_create(category_list)

    def test_pagination(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token}')
        data = json.loads(res.content)
        categorys_per_page = len(data['results'])
        total_categorys = data['count']
        next_page = data['next']
        self.assertEqual(total_categorys, 53)
        self.assertEqual(categorys_per_page, 50)
        self.assertIn('page=2', next_page)

    def test_get_categorys(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token}')
        self.assertEqual(json.loads(res.content)['results'][0]['name'], 'category52')


class TestListCreateTestQuizAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1')

        cls.question_data = {
            'text_question': 'text',
            'choise1': 'test1',
            'choise2': 'test2',
            'choise3': 'test3',
            'choise4': 'test4',
            'correct_choise': 1,
            'point': 1.75
        }
        cls.quiz_data1 = {
            'name': 'quiz1',
            'categorys': [1,],
            'questions': [1,],
            'time': '00:05:22',
            'start_at': '2025-02-02T00:05:22Z', 
            'end_at': '2025-02-03T00:05:22Z',
            'creator': cls.user1
        }

        cls.user2 = User.objects.create_user(username='user2')
        cls.token1 = Token.objects.create(user=cls.user1).key
        cls.token2 = Token.objects.create(user=cls.user2).key
        cls.question1_user1 = TestQuestion.objects.create(creator=cls.user1, **cls.question_data)
        cls.question2_user2 = TestQuestion.objects.create(creator=cls.user2, **cls.question_data)
        cls.category1 = Category.objects.create(name='cat1', slug='cat1')
        cls.url = reverse('quiz:test-quiz-list-create')
        cls.login_url = reverse('auth:login-token')

        quiz1, quiz2 = cls.quiz_data1.copy(), cls.quiz_data1.copy()
        quiz2['name'] = 'new quiz'
        quiz2['time'] = '00:02:00'
        quiz2['start_at'] = '2025-02-03T00:05:22Z'
        quiz2['end_at'] = '2025-02-04T00:05:22Z'
        del quiz1['categorys']
        del quiz1['questions']
        del quiz2['categorys']
        del quiz2['questions']

        tq1 = TestQuiz.objects.create(**quiz1)
        tq2 = TestQuiz.objects.create(**quiz2)
        tq1.categorys.add(1)
        tq1.questions.add(1)
        tq2.categorys.add(1)
        tq2.questions.add(1)

    def test_create_quiz_success_with_own_question(self):
        res = self.client.post(self.url, self.quiz_data1, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(res.status_code, 201)

    def test_create_quiz_error_use_your_own_question(self):
        quiz_data1 = self.quiz_data1
        quiz_data1['questions'] = [2, ]

        res = self.client.post(self.url, quiz_data1, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content)['questions'][0], 'you can only use your own questions.')

    def test_create_quiz_error_required_fields(self):
        res = self.client.post(self.url, HTTP_AUTHORIZATION = f'Token {self.token1}')
        data = json.loads(res.content)
        required_fields = ['name', 'time', 'start_at', 'end_at', 'questions']
        for field in required_fields:
            with self.subTest(field=field):
                self.assertEqual(data[field][0], 'This field is required.')

    def test_create_quiz_error_invalid_categorys(self):
        quiz_data1 = self.quiz_data1
        quiz_data1['categorys'] = [5,]

        res = self.client.post(self.url, quiz_data1, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content)['categorys'][0], 'Invalid pk "5" - object does not exist.')

    def test_create_quiz_error_invalid_questions(self):
        quiz_data1 = self.quiz_data1
        quiz_data1['questions'] = [5,]

        res = self.client.post(self.url, quiz_data1, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content)['questions'][0], 'Invalid pk "5" - object does not exist.')

    def test_get_all_quiz_user(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(res.status_code, 200)

    def test_pagination(self):
        del self.quiz_data1['questions']
        del self.quiz_data1['categorys']
        for i in range(56):
            tq = TestQuiz.objects.create(**self.quiz_data1)
            tq.categorys.set([1,])
            tq.questions.set([1,])


        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token1}')
        data = json.loads(res.content)
        total_results = data['count']
        item_per_page = len(data['results'])
        self.assertEqual(total_results, 58)
        self.assertEqual(item_per_page, 50)

    def test_filter_time(self):
        filter_time = '?max_time=00:03:00'
        res = self.client.get(self.url + filter_time, HTTP_AUTHORIZATION=f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 1)

        filter_time = '?min_time=00:02:50'
        res = self.client.get(self.url + filter_time, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 1)

        filter_time = '?exact_time=00:02:00'
        res = self.client.get(self.url + filter_time, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 1)

    def test_filter_name(self):
        filter_name = '?name__contains=1'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 1)

        filter_name = '?name__startswith=new'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 1)

    def test_filter_questions(self):
        filter_name = '?questions=1'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 2)

        filter_name = '?questions=2'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 0)

        filter_name = '?questions=20'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['questions'][0], 'Select a valid choice. 20 is not one of the available choices.')

    def test_filter_categorys(self):
        filter_name = '?categorys=1'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['count'], 2)

        filter_name = '?categorys=20'
        res = self.client.get(self.url + filter_name, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['categorys'][0], 'Select a valid choice. 20 is not one of the available choices.')


class TestRetriveUpdateTestQuiz(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        cls.token1 = Token.objects.create(user=user1).key
        cls.token2 = Token.objects.create(user=user2).key
        question = TestQuestion.objects.create(
            text_question = 'test1',
            choise1 = 'hello',
            choise2 = 'by',
            choise3 = 'buy',
            choise4 = 'sel',
            correct_choise = 1,
            creator = user1,
            point = 2.2
        )
        quiz = TestQuiz.objects.create(
            name = 'quiz1',
            time = '00:02:00',
            start_at = '2025-02-02T01:00:00Z',
            end_at = '2025-02-03T01:00:00Z',
            creator = user1
        )
        quiz.questions.add(question)
        cls.url = reverse('quiz:test-quiz-retrive-update', kwargs={'pk': 1})
        cls.login_url = reverse('auth:login-token')

    def test_retrive_creator(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token1}')
        self.assertEqual(json.loads(res.content)['name'], 'quiz1')
        self.assertIsInstance(json.loads(res.content)['questions'][0], dict)
        self.assertIn('correct_choise', json.loads(res.content)['questions'][0].keys())

    def test_retrive_no_creator(self):
        res = self.client.get(self.url, HTTP_AUTHORIZATION = f'Token {self.token2}')
        self.assertEqual(json.loads(res.content)['name'], 'quiz1')

    def test_update(self):
        data = {
            'name': 'quiz2',
            'time': '00:03:00',
            'start_at': '2025-02-02T01:00:00Z',
            'end_at': '2025-02-03T01:00:00Z',
            'questions': [1]
            # 'creator': 2
        }
        res = self.client.put(self.url, data, HTTP_AUTHORIZATION = f'Token {self.token1}')
        quiz = json.loads(res.content)
        self.assertEqual(quiz['name'], 'quiz2')
        self.assertEqual(quiz['time'], '00:03:00')
