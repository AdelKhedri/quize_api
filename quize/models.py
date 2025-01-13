from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='دسته بندی ریشه')
    allow_quiz_assignment = models.BooleanField(default=True, verbose_name='اجازه ارتباط آزمون با این دسته بندی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['-id']


    def __str__(self):
        return self.name


class TestQuestion(models.Model):
    choises_list = ((1, 1), (2, 2), (3, 3), (4, 4))

    text_question = models.CharField(max_length=500, verbose_name='متن سوال')
    image_question = models.ImageField(upload_to='images/test_questions/', blank=True, verbose_name='عکس سوال')
    choise1 = models.CharField(max_length=200, verbose_name='گزینه 1')
    choise2 = models.CharField(max_length=200, verbose_name='گزینه 2')
    choise3 = models.CharField(max_length=200, verbose_name='گزینه 3')
    choise4 = models.CharField(max_length=200, verbose_name='گزینه 4')
    correct_choise = models.IntegerField(choices=choises_list, verbose_name='گزینه درست')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name = 'سازنده')
    point = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='نمره')

    class Meta:
        verbose_name = 'سوال تستی'
        verbose_name_plural = 'سوالات تستی'
        ordering = ['-id']


    def __str__(self):
        return 'Qid: {}-- U: {}'.format(self.id, self.creator.__str__())


class BaseQuiz(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام آزمون')
    poster = models.ImageField(upload_to='images/test_quiz/poster/', blank=True, verbose_name='پوستر آزمون')
    categorys = models.ManyToManyField(Category, blank = True, verbose_name='دسته بندی')
    time = models.TimeField(verbose_name='زمان آزمون')
    start_at = models.DateTimeField(verbose_name = 'زمان شروع')
    end_at = models.DateTimeField(verbose_name = 'زمان پایان')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name = 'سازنده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')

    class Meta:
        abstract = True


class TestQuiz(BaseQuiz):
    questions = models.ManyToManyField(TestQuestion, verbose_name='سوالات')

    class Meta:
        verbose_name = 'آزمون تستی'
        verbose_name_plural = 'آزمون های تستی'
        ordering = ['-created_at']

    def __str__(self):
        return f'Q: {self.name}-- U: {self.creator.__str__()}'


class UserResponseTestQuiz(models.Model):
    choises_list = ((1, 1), (2, 2), (3, 3), (4, 4))

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    quiz = models.ForeignKey(TestQuiz, on_delete=models.CASCADE, verbose_name='آزمون')
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, verbose_name='سوال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    choise = models.IntegerField(choices=choises_list, verbose_name='انتخاب کاربر')
    point = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='نمره')

    class Meta:
        verbose_name = 'پاسخ سوال آزمون تستی'
        verbose_name_plural = 'پاسخ سوالات آزمون تستی'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user}: {self.quiz.name}: {self.question.id}'


class UserStartedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    quiz = models.ForeignKey(TestQuiz, on_delete=models.CASCADE, verbose_name='آزمون')
    started = models.DateTimeField(auto_now_add=True, verbose_name='زمان شروع')
    total_point = models.DecimalField(default=0, max_digits=4, decimal_places=2, verbose_name='نمره کلی')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ['started']

    def __str__(self):
        return self.quiz.__str__()
