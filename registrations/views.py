from .models import Reverberate, DebReverberate
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
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
                teamname=request.data.get('teamname')
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
class deb_register_check_email(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            email = request.GET.get('email', None)
            registration = DebReverberate.objects.get(email=email)
            if registration:
                return Response({ "success": False }, safe=False)
            return Response({ "success": True })
        except:
            return Response({ "success": True })

@permission_classes(
    [
        AllowAny,
    ]
)
class register_check_email(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        registered = {
            "rev": False,
            "whatif": False
        }
        try:
            email = request.GET.get('email', None)
            registration = Reverberate.objects.get(email=email)
            if registration:
                registered["rev"] = True
        except:
            pass

        try:
            email = request.GET.get('email', None)
            registration = DebReverberate.objects.get(email=email)
            if registration:
                registered["whatif"] = True
        except:
            pass

        return Response({ "data": registered })