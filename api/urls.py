from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('login/', csrf_exempt(views.login.as_view()), name='login'),
    path('register/', csrf_exempt(views.register.as_view()), name='register'),
    path('question/', csrf_exempt(views.question.as_view()), name='question'),
    path('answer/', csrf_exempt(views.answer.as_view()), name='answer'),
    path('clue/', csrf_exempt(views.clue.as_view()), name='clue'),
    path('leaderboard/', csrf_exempt(views.leaderboard.as_view()), name='leaderboard')
]