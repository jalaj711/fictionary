from django.db import models

# Create your models here.
class Question(models.Model):
    text = models.TextField()
    round = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=100)
    media = models.FileField(upload_to="media/questions", blank=True, null=True)

class Clues(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    content = models.TextField()

class User(models.Model):
    username = models.TextField(null=False, blank=False, unique=True, primary_key=True)
    password = models.TextField(null=False, blank=False)
    salt = models.TextField(null=False, blank=False)
    current_round = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='current_round')
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Meta(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class AccessTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    token = models.TextField(null=False, blank=False)
    expires_on = models.DateTimeField(null=False, blank=False)