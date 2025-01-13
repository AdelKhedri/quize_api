from datetime import timedelta
from decimal import Decimal
from rest_framework import serializers
from .models import Category, TestQuestion, TestQuiz, UserResponseTestQuiz, UserStartedQuiz
from django.utils import timezone


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


class UserResponseTestQuizSerializer(serializers.Serializer):
    choises = ((1, 1), (2, 2), (3, 3), (4, 4))

    question = serializers.PrimaryKeyRelatedField(queryset = TestQuestion.objects.all())
    quiz = serializers.PrimaryKeyRelatedField(queryset = TestQuiz.objects.all())
    choise = serializers.ChoiceField(choices=choises)

    def save(self, **kwargs):
        quiz = self.validated_data.get('quiz', None)
        question = self.validated_data.get('question', None)
        choise = self.validated_data.get('choise', None)
        user = self.context['request'].user

        if question and choise and quiz:
            if quiz.start_at > timezone.now():
                raise serializers.ValidationError({'quiz': 'quiz is not started.'})
            elif quiz.end_at < timezone.now():
                raise serializers.ValidationError({'quiz': 'quiz is ended.'})
            elif question not in quiz.questions.all():
                raise serializers.ValidationError({'question': 'only questions that in quiz.'})
            else:
                start_quiz, created = UserStartedQuiz.objects.get_or_create(user=user, quiz=quiz)
                if timezone.now() > start_quiz.started + timedelta(hours=quiz.time.hour, minutes=quiz.time.minute, seconds=quiz.time.second):
                    raise serializers.ValidationError({'quiz': 'time to complete quiz is ended.'})

            ques = UserResponseTestQuiz.objects.filter(user=user, quiz=quiz, question=question)
            if ques.exists():
                ques.update(choise=choise)
                return ques.first()
            else:
                point = question.point if choise == question.correct_choise else 0
                start_quiz.total_point = start_quiz.total_point + Decimal(point)
                start_quiz.save()
                return UserResponseTestQuiz.objects.create(user=user, question=question, quiz=quiz, choise=choise, point=point)


class UserStartedQuizNoAnswerSerializer(serializers.ModelSerializer):
    quiz = TestQuizUpdateSerializer()
    details = serializers.HyperlinkedIdentityField(view_name='quiz:quiz-result-detail')

    class Meta:
        model = UserStartedQuiz
        exclude = ['user']


class UserStartedQuizWithAnswerSerializer(serializers.ModelSerializer):
    quiz = TestQuizQuestionWithAnswerSerializer()

    class Meta:
        model = UserStartedQuiz
        exclude = ['user']
