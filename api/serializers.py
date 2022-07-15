from rest_framework import serializers
from .models import Question, Clues


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class CluesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clues
        fields = "__all__"