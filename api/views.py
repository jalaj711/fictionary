from datetime import datetime
from django.db.utils import IntegrityError
from django.http import JsonResponse
from .serializers import *
from .models import User, Question, Clues
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from knox.models import AuthToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Create your views here.


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
                return Response("Username already used!!", status=status.HTTP_400_INTERNAL_SERVER_ERROR)
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
            question = Question.objects.get(round=cround)
            try:
                media = question.media.url
            except ValueError:
                media = ''
            return JsonResponse({
                'text': question.text,
                'round': question.round,
                'media': media
            })
        except IntegrityError:
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
            clues = Clues.objects.filter(question=question)
            clues = [clue.content for clue in clues]
            return JsonResponse({
                'clues': clues,
            })
        except IntegrityError:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)

@permission_classes(
    [IsAuthenticated]
)
class answer(generics.GenericAPIView):
    def post(self, request):
        cround = request.user.current_round

        if 'answer' not in request.data.keys():
            return JsonResponse({'message': 'Empty answer not accepted'}, status=status.HTTP_400_BAD_REQUEST)
        
        answer = request.data.get('answer').lower().strip()

        try:
            question = Question.objects.get(round=cround)
            if question.answer == answer:
                request.user.current_round = cround + 1
                request.user.points += 10
                request.user.time = datetime.now()
                request.user.save()
                return JsonResponse({
                    'success': True
                })

            return JsonResponse({
                'success': False
            })
        except IntegrityError:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)

@permission_classes(
    [IsAuthenticated]
)
class leaderboard(generics.GenericAPIView):
    def get(self, request):
        #try:
        leaderboard = list(User.objects.filter().order_by('-points'))

        # Tie breaker in case of same points
        for i in range(len(leaderboard)):
            for j in range(i, len(leaderboard)):
                if leaderboard[i].points == leaderboard[j].points:
                    if leaderboard[i].time > leaderboard[j].time:
                        leaderboard[i], leaderboard[j] = leaderboard[j], leaderboard[i]
        
        leaderboard = [{'name': user.username, 'points': user.points} for user in leaderboard]

        return JsonResponse({
            'leaderboard': leaderboard
            })
        # except:
        #     return JsonResponse({
        #         'message': 'Server failed to process the request'
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

