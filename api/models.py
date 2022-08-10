from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Question(models.Model):
    text = models.TextField()
    clue = models.TextField(default='', blank=True, null=True)
    clue_wait_time = models.IntegerField(default=5)
    round = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=100)
    media = models.FileField(upload_to="questions/", blank=True, null=True)
    points = models.IntegerField(default=10)


class User(AbstractUser):
    current_round = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    calc_wait_time_from = models.DateTimeField(blank=True, null=True)

class Meta(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
