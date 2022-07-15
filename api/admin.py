from django.contrib import admin
from .models import User, Question, Clues, AccessTokens, Meta
# Register your models here.

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Clues)
admin.site.register(AccessTokens)
admin.site.register(Meta)