import bcrypt
import datetime
import os
import hashlib
from .models import User, AccessTokens, Question

def create_new_user(username, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt).decode('utf-8')
    user = User.objects.create(username=username, salt=salt, password=hashed, current_round=Question.objects.get(round=1))
    return user

def login_user(username, password):
    try:
        search = User.objects.get(username=username)
        if bcrypt.checkpw(password.encode(), search.password.encode()):
            token = hashlib.sha256(os.urandom(24)).hexdigest()
            AccessTokens.objects.create(user=search, token=token, expires_on=datetime.datetime.now() + datetime.timedelta(days=30))
            return token
        else:
            return False
    except User.DoesNotExist:
        return False

def verify_token(token):
    try:
        tkn = AccessTokens.objects.get(token=token)
        return tkn.user
    except AccessTokens.DoesNotExist:
        return False

def log_out(token):
    try:
        tkn = AccessTokens.objects.get(token=token)
        tkn.delete()
    except AccessTokens.DoesNotExist:
        return False