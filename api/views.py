import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
from .serializers import *
from .models import User, Question, Clues, AccessTokens
from . import auth
# Create your views here.

def login(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    if not (username and password):
        return JsonResponse({"text": "Correct Values not provided"}, status=400)
    token = auth.login_user(username, password)
    if not token:
        return JsonResponse({"text": "Invalid login credentials"}, status=401)
    return JsonResponse({"token": token})

def register(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    if not (username and password):
        return JsonResponse({"text": "Correct Values not provided"}, status=400)
    try:
        auth.create_new_user(username, password)
        token = auth.login_user(username, password)
        return JsonResponse({"token": token})
    except IntegrityError:
        return JsonResponse({"text": "Username is already in use"}, status=400)