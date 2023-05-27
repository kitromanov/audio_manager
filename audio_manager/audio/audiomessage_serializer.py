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

    @staticmethod
    def get_duration(file_name):
        audio = mutagen.File(file_name)
        if type(audio) == mutagen.mp3.MP3:
            duration_in_seconds = audio.info.length
            return timedelta(seconds=duration_in_seconds)
        else:
            raise ValueError('Unsupported audio format')

    def create(self, validated_data):
        audio_file = validated_data.pop('audio_file')
        file_name = default_storage.save(audio_file.name, audio_file)
        instance = super().create(validated_data)
        instance.audio_file = audio_file
        instance.duration = self.get_duration(file_name)
        recognition = RecognitionLongAudio(
            api_key=os.getenv("API_KEY"),
            bucket_name=os.getenv("BUCKET")
        )
        recognition.upload_to_bucket('', file_name)
        result = recognition.recognize(file_name)
        instance.text = recognition.get_text_transcription(*result)
        instance.save()
        default_storage.delete(file_name)
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
