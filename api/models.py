from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Question(models.Model):
    text = models.TextField()
    round = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=100)
    media = models.FileField(upload_to="questions/", blank=True, null=True)
    points = models.IntegerField(default=10)

class Clues(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    clue_no = models.IntegerField(blank=False, null=False)
    content = models.TextField()
    wait_time_in_minutes = models.IntegerField(default=5)

class User(AbstractUser):
    current_round = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    current_clue = models.IntegerField(default=0)
    calc_wait_time_from = models.DateTimeField(blank=True, null=True)

class Meta(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
