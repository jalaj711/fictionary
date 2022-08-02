from django.urls import path
from .models import Meta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import views

def _available_when_live(view_function, *args, **kwargs):
    meta = Meta.objects.filter()[0]
    now = timezone.now()
    if now > meta.start_time and now < meta.end_time:
        return view_function(*args, **kwargs)
    return JsonResponse({
        'message': "The game is not live"
    }, status=400)


def available_when_live(view_function):
    return lambda *args, **kwargs: _available_when_live(view_function, *args, **kwargs)


urlpatterns = [
    path('login/', csrf_exempt(views.login.as_view()), name='login'),
    path('register/', csrf_exempt(views.register.as_view()), name='register'),
    path('question/', csrf_exempt(available_when_live(views.question.as_view())), name='question'),
    path('answer/', csrf_exempt(available_when_live(views.answer.as_view())), name='answer'),
    path('clue/', csrf_exempt(available_when_live(views.clue.as_view())), name='clue'),
    path('leaderboard/', csrf_exempt(views.leaderboard.as_view()), name='leaderboard'),
    path('accounts/get-social-token/', csrf_exempt(views.sociallogin_get_token), name='social_token_generator')
]
