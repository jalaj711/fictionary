from datetime import timedelta
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .serializers import *
from .models import User, Question, Meta
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from knox.models import AuthToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from allauth.socialaccount.models import SocialAccount
import re
import hashlib

# @permission_classes([ AllowAny ])
# def social_generate_token(request):
#     if request.user.is_authenticated:
#         response = redirect('/')
#         response.set_cookie('token', AuthToken.objects.create(request.user)[1], expires=timezone.now() + timedelta(days=3))
#         return response
#     return HttpResponse('Not authenticated', status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([AllowAny])
class sociallogin_get_token(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        if(
            (data.get("email") and
             data.get("email_verified") and
             data.get("family_name") and
             data.get("given_name") and
             data.get("name") and
             data.get("picture"))
                is None):
            return HttpResponse('Not authenticated', status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(email=data.get("email"))
            except User.DoesNotExist:
                user = User.objects.create(email=data.get(
                    "email"), first_name=data["given_name"], last_name=data["family_name"], picture=data["picture"], username=hashlib.md5(data["email"].encode()).hexdigest())
            return Response({
                "success": True,
                "token": AuthToken.objects.create(user)[1]
            })


@permission_classes([AllowAny])
def check_game_live(request):
    meta = Meta.objects.filter()[0]
    now = timezone.now()
    if now > meta.start_time and now < meta.end_time:
        return JsonResponse({
            'game_live': True,
            'date': meta.end_time
        })
    return JsonResponse({
        'game_live': False,
        'date': meta.start_time
    })


@permission_classes(
    [AllowAny]
)
def leaderboard(request):
    # try:
    leaderboard = list(User.objects.filter().order_by('-points', 'time'))

    # Tie breaker in case of same points
    # for i in range(len(leaderboard)):
    #     for j in range(i, len(leaderboard)):
    #         if leaderboard[i].points == leaderboard[j].points:
    #             if leaderboard[i].time > leaderboard[j].time:
    #                 leaderboard[i], leaderboard[j] = leaderboard[j], leaderboard[i]
    board = []
    for user in leaderboard:
        try:
            if user.first_name and user.last_name and user.picture:
                board.append({'username': user.username, 'name': user.first_name +
                          ' ' + user.last_name, 'points': user.points, "avatar": user.picture})
        except:
            continue

    return JsonResponse({
        'leaderboard': board
    })
    # except:
    #     return JsonResponse({
    #         'message': 'Server failed to process the request'
    #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes(
    [
        AllowAny,
    ]
)
class register(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if (
            request.data.get("username") != ""
            and request.data.get("password") != ""
        ):
            try:
                user = User.objects.create_user(
                    username=request.data.get("username"),
                    password=request.data.get("password")
                )
            except:
                return Response("Username already used!!", status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        return Response(
            "Username and password are required fields", status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes(
    [
        AllowAny,
    ]
)
class login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if user is not None:
            return Response(
                {
                    "user": LoginSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        else:
            return Response(
                "Wrong Credentials! Please try again.", status=status.HTTP_403_FORBIDDEN
            )


@permission_classes(
    [IsAuthenticated]
)
class question(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            if cround > Question.objects.filter().count():
                return JsonResponse({
                    'gameOver': True,
                    'message': 'Game is over'
                })
            question = Question.objects.get(round=cround)
            try:
                media = question.media.url
            except ValueError:
                media = ''

            # To make sure that the wait_time is not reset everytime a
            # user fetches the question, for example when refreshing the page
            if request.user.calc_wait_time_from is None:
                request.user.calc_wait_time_from = timezone.now()
                request.user.save()

            return JsonResponse({
                'text': question.text,
                'round': question.round,
                'media': media
            })
        except Model.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)


@permission_classes(
    [IsAuthenticated]
)
class clue(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            question = Question.objects.get(round=cround)
        except Question.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Make sure that enough time has passed for the user
        diff = timezone.now() - request.user.calc_wait_time_from
        print(timezone.now(), request.user.calc_wait_time_from, diff)
        if diff > timedelta(minutes=question.clue_wait_time):
            return JsonResponse({
                'clue': question.clue,
                'success': True
            })
        else:
            return JsonResponse({
                'message': f'Wait for {question.clue_wait_time * 60 - diff.seconds} more second(s) to view your clue.',
                'timeleft': question.clue_wait_time * 60 - diff.seconds,
                'success': False
            })


@permission_classes(
    [IsAuthenticated]
)
class checkClueAvailability(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            question = Question.objects.get(round=cround)
        except Question.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Make sure that enough time has passed for the user
        diff = timezone.now() - request.user.calc_wait_time_from
        print(timezone.now(), request.user.calc_wait_time_from, diff)
        if diff > timedelta(minutes=question.clue_wait_time):
            return JsonResponse({
                'available': True,
                'success': True
            })
        else:
            return JsonResponse({
                'available': False,
                'timeleft': question.clue_wait_time * 60 - diff.seconds,
                'success': True
            })


@permission_classes(
    [IsAuthenticated]
)
class answer(generics.GenericAPIView):
    def post(self, request):
        cround = request.user.current_round

        if 'answer' not in request.data.keys():
            return JsonResponse({'message': 'Empty answer not accepted'}, status=status.HTTP_400_BAD_REQUEST)

        answer = request.data.get('answer').lower().strip()
        answer = re.sub(' +', ' ', answer)

        try:
            question = Question.objects.get(round=cround)
            if(len(question.answer.split(',')) > 1):
                if answer in question.answer.split(','):
                    # Increment points
                    request.user.current_round = cround + 1
                    request.user.points += question.points
                    request.user.time = timezone.now()
                    request.user.calc_wait_time_from = None

                    request.user.save()
                    return JsonResponse({
                        'success': True
                    })
            if question.answer == answer:

                # Increment points
                request.user.current_round = cround + 1
                request.user.points += question.points
                request.user.time = timezone.now()
                request.user.calc_wait_time_from = None

                request.user.save()
                return JsonResponse({
                    'success': True
                })

            return JsonResponse({
                'success': False
            })
        except Model.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)
