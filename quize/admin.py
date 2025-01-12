from django.contrib import admin
from .models import Category, TestQuestion, TestQuiz

admin.site.register(Category)
admin.site.register(TestQuestion)
admin.site.register(TestQuiz)
