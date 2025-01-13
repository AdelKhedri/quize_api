from django.contrib import admin
from .models import Category, TestQuestion, TestQuiz, UserResponseTestQuiz, UserStartedQuiz

admin.site.register(Category)
admin.site.register(TestQuestion)
admin.site.register(TestQuiz)
admin.site.register(UserResponseTestQuiz)
admin.site.register(UserStartedQuiz)
