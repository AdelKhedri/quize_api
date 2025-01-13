from django.urls import path
from .views import (ListCreateTestQuestionAPI, RetriveUpdateTestQuestionAPI, ListCreateTestQuizAPI, RetriveUpdateTestQuizAPI, ListCategorysAPI
                    , ListAllQuizAPI, CreateUserResponseTestQuizAPI, AllUserStartedQuizAPI)


app_name = 'quiz'
urlpatterns = [
    path('test/question/list-create/', ListCreateTestQuestionAPI.as_view(), name='test-question-list-create'),
    path('test/question/<int:pk>/', RetriveUpdateTestQuestionAPI.as_view(), name='test-question-retrive-update'),
    path('test/quiz/list-create/', ListCreateTestQuizAPI.as_view(), name='test-quiz-list-create'),
    path('test/quiz/<int:pk>/', RetriveUpdateTestQuizAPI.as_view(), name='test-quiz-retrive-update'),
    path('test/quiz/response/', CreateUserResponseTestQuizAPI.as_view(), name='set-test-quiz-respons'),
    path('test/quiz/all', ListAllQuizAPI.as_view(), name='quiz-list'),
    path('test/quiz/result', AllUserStartedQuizAPI.as_view(), name='quiz-result'),
    path('categorys', ListCategorysAPI.as_view(), name='categorys-list'),
]