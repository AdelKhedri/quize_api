import django_filters
from .models import TestQuize


class QuizeFilter(django_filters.FilterSet):
    class Meta:
        model = TestQuize
        fields = ['name', 'categorys', 'start_at', 'end_at', 'creator', 'created_at']