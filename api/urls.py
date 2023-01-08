from django.urls import path
from .models import Meta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import views


def _available_when_live(view_function, check_end, *args, **kwargs):
    meta = Meta.objects.filter()[0]
    now = timezone.now()
    if now > meta.start_time:
        if not check_end:
            return view_function(*args, **kwargs)
        elif now < meta.end_time:
            return view_function(*args, **kwargs)
        else:
            return JsonResponse({
                'game_not_live': True,
                'message': "The game is not live",
                'time_up': True
            }, status=400)

    return JsonResponse({
        'game_not_live': True,
        'message': "The game is not live"
    }, status=400)


def available_when_live(view_function, check_end=True):
    return lambda *args, **kwargs: _available_when_live(view_function, check_end, *args, **kwargs)


urlpatterns = [
    path('check-game-live/', csrf_exempt(views.check_game_live), name='isGameLive'),
    path('login/', csrf_exempt(views.login.as_view()), name='login'),
    path('register/', csrf_exempt(views.register.as_view()), name='register'),
    path('question/', csrf_exempt(available_when_live(views.question.as_view())), name='question'),
    path('answer/', csrf_exempt(available_when_live(views.answer.as_view())), name='answer'),
    path('clue/', csrf_exempt(available_when_live(views.clue.as_view())), name='clue'),
    path('check-clue-available/', csrf_exempt(available_when_live(
        views.checkClueAvailability.as_view())), name='clueAvailability'),
    path('leaderboard/', csrf_exempt(views.leaderboard), name='leaderboard'),
    path('accounts/get-social-token/',
         csrf_exempt(views.sociallogin_get_token.as_view()), name='social_token_generator')
]
