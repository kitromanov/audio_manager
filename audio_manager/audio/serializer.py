import time

from rest_framework import serializers

from audio.models import *
from audio.recognition import RecognitionLongAudio
from datetime import timedelta
import mutagen
from django.core.files.storage import default_storage
import os
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from dotenv import load_dotenv

load_dotenv()


class AudioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioMessage
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator'] = user

        return super().create(validated_data)


class TagSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = AudioMessage
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
