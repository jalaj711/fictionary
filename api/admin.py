from django.contrib import admin
from .models import User, Question, Clues, AccessTokens, Meta
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Clues)
admin.site.register(AccessTokens)
admin.site.register(Meta)