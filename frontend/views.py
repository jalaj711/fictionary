from django.http import HttpResponse
from django.conf import settings
import os

# Create your views here.
def index(request):
    html_content = open(os.path.join(settings.STATIC_ROOT, "index.html"))
    return HttpResponse(html_content)


def handler404(*args, **kwargs):
    html_content = open(os.path.join(settings.STATIC_ROOT, "index.html"))
    return HttpResponse(html_content, status=200)