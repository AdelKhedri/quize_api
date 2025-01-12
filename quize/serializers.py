from rest_framework import serializers
from .models import Category, TestQuestion, TestQuiz


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TestQuizUpdateSerializer(serializers.ModelSerializer):
    ''' ### With questions id for update and create '''
    creator = serializers.SlugRelatedField(slug_field = 'username', read_only=True)

    class Meta:
        model = TestQuiz
        fields = '__all__'

    def validate_questions(self, questions):
        for question in questions:
            if question and question.creator != self.context['request'].user:
                raise serializers.ValidationError('you can only use your own questions.')
        return questions

    def validate_categorys(self, categorys):
        for category in categorys:
            if not category:
                raise serializers.ValidationError('category {} does not exist.'.format(category.id))
            elif category and not category.allow_quiz_assignment:
                raise serializers.ValidationError('you can only use categorys with attr allow_quiz_assignment')
        return categorys

    def save(self, **kwargs):
        questions = self.validated_data.pop('questions', [])
        categorys = self.validated_data.pop('categorys', [])
        ins = super().save(**kwargs)
        ins.questions.set(questions)
        ins.categorys.set(categorys)
        return ins

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TestQuizQuestionNoAnswerSerializer(serializers.ModelSerializer):
    ''' ### With question object without answer
     this serializer for **doing Test**
       '''
    questions = TestQuestionNoAnswerSerializer(many = True)
    categorys = CategorySerializer(many = True)

    class Meta:
        model = TestQuiz
        fields = '__all__'


class TestQuizQuestionWithAnswerSerializer(TestQuizQuestionNoAnswerSerializer):
    ''' ### With question object with answer for **Creator** '''

    questions = TestQuestionWithAnswerSerializer(many = True)
