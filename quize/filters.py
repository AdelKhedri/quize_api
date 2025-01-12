import django_filters
from django_filters import rest_framework as filters
from .models import TestQuiz


class QuizFilter(django_filters.FilterSet):
    max_time = filters.TimeFilter(field_name='time', lookup_expr='lte', label='max')
    min_time = filters.TimeFilter(field_name='time', lookup_expr='gte')
    exact_time = filters.TimeFilter(field_name='time', lookup_expr='exact')

    class Meta:
        model = TestQuiz
        fields = {
            'name': ['contains', 'startswith',],
            'questions': ['exact'],
            'categorys': ['exact'],
            # 'time': ['exact', 'gte', 'lte'],
            'end_at': ['gte', 'lte'],
            'start_at': ['gte', 'lte'],
            'created_at': ['gte', 'lte'],
        }
