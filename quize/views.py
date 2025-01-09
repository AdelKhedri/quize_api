from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TestQuestionWithAnswerSerializer
from .models import TestQuestion


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
