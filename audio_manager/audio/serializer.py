import time

from rest_framework import serializers

from audio.models import *
from audio.recognition import RecognitionLongAudio
from datetime import timedelta
import mutagen
from django.core.files.storage import default_storage
import os
from dotenv import load_dotenv

load_dotenv()


# TODO: add celery
# TODO: add .ogg parsing
# TODO: adding by URL
class AudioMessageSerializer(serializers.ModelSerializer):

    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AudioMessage
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
