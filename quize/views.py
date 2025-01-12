from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TestQuestionWithAnswerSerializer, TestQuizUpdateSerializer, TestQuizQuestionNoAnswerSerializer, TestQuizQuestionWithAnswerSerializer, TestQuiz, CategorySerializer
from .models import Category, TestQuestion, TestQuiz
from django.utils import timezone
from django_filters import rest_framework as filters
from .filters import QuizFilter


class ListCreateTestQuestionAPI(ListCreateAPIView):
    serializer_class = TestQuestionWithAnswerSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCreator]

    def get_queryset(self):
        return TestQuestion.objects.filter(creator = self.request.user)


class RetriveUpdateTestQuestionAPI(RetrieveUpdateAPIView):
    serializer_class = TestQuestionWithAnswerSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    queryset = TestQuestion


# Quiz
class ListCreateTestQuizAPI(ListCreateAPIView):
    serializer_class = TestQuizUpdateSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    queryset = TestQuiz.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = QuizFilter

    # def get_queryset(self):
    #     return TestQuiz.objects.filter(creator = self.request.user)


class RetriveUpdateTestQuizAPI(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TestQuiz.objects.all()

    def get_serializer_class(self):
        quiz = self.get_object()
        user = self.request.user

        if self.request.method == 'GET':
            if user == quiz.creator:
                return  TestQuizQuestionWithAnswerSerializer
            elif quiz.start_at <= timezone.now() <= quiz.end_at:
                return TestQuizQuestionNoAnswerSerializer 
            else:
                return TestQuizUpdateSerializer
        elif self.request.method == 'PUT':
            if user == quiz.creator:
                return TestQuizUpdateSerializer
            raise self.permission_denied(self.request, f'only the creator of the {quiz.__class__.__name__} can edit it')


class ListCategorysAPI(ListAPIView):
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()


class ListAllQuizAPI(ListAPIView):
    serializer_class = TestQuizUpdateSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TestQuiz.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = QuizFilter

# TODO: CreateUserAnswer
# TODO: See quiz result
# TODO: See all Quiz signin