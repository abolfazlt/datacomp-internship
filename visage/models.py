from django.contrib.auth.models import User
from django.db import models


class Competition(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='title')
    description = models.TextField(verbose_name='description')


class Problem(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='title')
    description = models.TextField(verbose_name='description')
    data = models.FileField(verbose_name='data')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='competition', null=True)


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='problem')
    file = models.FileField(verbose_name='file')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='timestamp')
    error = models.FloatField(null=True, blank=True, db_index=True, verbose_name='error')
    is_final = models.BooleanField(default=False, verbose_name='is final')

    SUBMISSION_STATUS = (
        ('S', 'Submitted'),
        ('P', 'Processing'),
        ('E', 'Error'),
        ('J', 'Judged'),
    )
    status = models.CharField(
        max_length=1, choices=SUBMISSION_STATUS, default='S', db_index=True, verbose_name='status'
    )
