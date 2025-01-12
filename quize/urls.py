from django.urls import path
from .views import (ListCreateTestQuestionAPI, RetriveUpdateTestQuestionAPI, ListCreateTestQuiezeAPI, RetriveUpdateTestQuizAPI, ListCategorysAPI,)


app_name = 'quiz'
urlpatterns = [
    path('test/question/list-create/', ListCreateTestQuestionAPI.as_view(), name='test-question-list-create'),
    path('test/question/<int:pk>/', RetriveUpdateTestQuestionAPI.as_view(), name='test-question-retrive-update'),
    path('test/quiz/list-create/', ListCreateTestQuiezeAPI.as_view(), name='test-quiz-list-create'),
    path('test/quiz/<int:pk>/', RetriveUpdateTestQuizAPI.as_view(), name='test-quiz-retrive-update'),
    path('categorys', ListCategorysAPI.as_view(), name='categorys-list'),
]