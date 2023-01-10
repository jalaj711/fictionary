from .models import Reverberate, DebReverberate
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.utils import IntegrityError

# Create your views here.


@permission_classes(
    [
        AllowAny,
    ]
)
class register(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            Reverberate.objects.create(
                email=request.data.get('email'),
                name=request.data.get('name'),
                number=request.data.get('number'),
                section=request.data.get('section'),
                roll_no=request.data.get('roll_no'),
            )
            return Response({"success": True})
        except IntegrityError as e:
            print(e)
            return Response({"success": False, "message": "Not all fields were provided"})

@permission_classes(
    [
        AllowAny,
    ]
)
class deb_register(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            DebReverberate.objects.create(
                email=request.data.get('email'),
                name=request.data.get('name'),
                number=request.data.get('number'),
                section=request.data.get('section'),
                roll_no=request.data.get('roll_no'),
            )
            return Response({"success": True})
        except IntegrityError as e:
            print(e)
            return Response({"success": False, "message": "Not all fields were provided"})

