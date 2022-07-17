from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Question(models.Model):
    text = models.TextField()
    round = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=100)
    media = models.FileField(upload_to="media/questions", blank=True, null=True)

class Clues(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    content = models.TextField()

class User(AbstractUser):
    current_round = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Meta(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
