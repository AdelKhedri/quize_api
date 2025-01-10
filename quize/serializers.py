from rest_framework import serializers
from .models import Category, TestQuestion


class TestQuestionWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        exclude = ['creator']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
