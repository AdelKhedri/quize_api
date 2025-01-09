from django.db import models
from django.contrib.auth.models import User


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
