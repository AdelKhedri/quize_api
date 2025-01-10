from django.urls import path
from .views import (ListCreateTestQuestionAPI, RetriveUpdateTestQuestionAPI, ListCategorysAPI,)


app_name = 'quize'
urlpatterns = [
    path('test/question/list-create/', ListCreateTestQuestionAPI.as_view(), name='test-question-list-create'),
    path('test/question/<int:pk>/', RetriveUpdateTestQuestionAPI.as_view(), name='test-question-retrive-update'),
    path('categorys', ListCategorysAPI.as_view(), name='categorys-list'),
]