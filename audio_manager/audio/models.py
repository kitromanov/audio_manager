import uuid
from datetime import timedelta

import mutagen

from django.core.files.storage import default_storage
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from audio import tasks
from audio.recognition import RecognitionLongAudio
from taggit.managers import TaggableManager
from user.models import User
import os
from dotenv import load_dotenv

load_dotenv()


def get_audio_messages_upload_path(instance, filename):
    unique_id = uuid.uuid4().hex
    file_path = f"{unique_id}_{filename}"
    return os.path.join('audio_messages', now().date().strftime("%Y/%m/%d"), file_path)


class AudioMessage(models.Model):
    assigned_users = models.ManyToManyField(User, blank=True, related_name='audio_messages_user')
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to=get_audio_messages_upload_path)
    file_name = models.CharField(max_length=255, default='file')
    text = models.TextField(blank=True)
    duration = models.DurationField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incoming_number = models.CharField(max_length=20)
    outgoing_number = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        verbose_name = _('audio message')
        verbose_name_plural = _('audio messages')

    def str(self):
        return self.text

    @staticmethod
    def get_duration(filename):
        audio = mutagen.File(filename)
        if type(audio) == mutagen.mp3.MP3:
            duration_in_seconds = audio.info.length
            return timedelta(seconds=duration_in_seconds)
        else:
            raise ValueError('Unsupported audio format')

    @staticmethod
    def get_audio_text(file_name):
        recognition = RecognitionLongAudio(
            api_key=os.getenv("API_KEY"),
            bucket_name=os.getenv("BUCKET")
        )
        recognition.upload_to_bucket('', file_name)
        result = recognition.recognize(file_name)
        return recognition.get_text_transcription(*result)

    def save(self, *args, **kwargs):
        file = default_storage.save(self.audio_file.name, self.audio_file)
        self.text = tasks.get_audio_text.delay(file).get()
        self.duration = self.get_duration(file)
        self.file_name = self.audio_file.name
        default_storage.delete(file)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
    audio_message = models.ForeignKey(AudioMessage, on_delete=models.CASCADE, related_name='comments_audio_message')
    text = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def str(self):
        return self.text
