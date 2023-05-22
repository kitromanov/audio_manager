from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class AudioMessage(models.Model):
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_messages_user')
    audio_file = models.FileField(upload_to='audio_messages/')
    audio_url = models.URLField()
    text = models.TextField(blank=True)
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incoming_number = models.CharField(max_length=20)
    outgoing_number = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('audio message')
        verbose_name_plural = _('audio messages')

    def __str__(self):
        return self.transcript


class Tag(models.Model):
    name = models.CharField(max_length=30)
    audio_messages = models.ManyToManyField(AudioMessage, related_name='tags_audio_message')

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
    audio_message = models.ForeignKey(AudioMessage, on_delete=models.CASCADE, related_name='comments_audio_message')
    text = models.TextField()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return self.text
