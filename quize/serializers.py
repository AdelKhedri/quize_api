from rest_framework import serializers
from .models import TestQuestion


class TestQuestionWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        exclude = ['creator']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TestQuestionNoAnswerSerializer(TestQuestionWithAnswerSerializer):
    class Meta(TestQuestionWithAnswerSerializer.Meta):
        exclude = ['creator', 'correct_choise']
