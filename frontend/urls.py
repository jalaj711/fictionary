from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<path>.*)/$', views.handler404, name="handler404")
]
