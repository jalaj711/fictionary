from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('reverberate/',
         csrf_exempt(views.register.as_view()), name='reverberate_registration'),
    path('rev-debate/',
         csrf_exempt(views.deb_register.as_view()), name='reverberate_registration')
]
