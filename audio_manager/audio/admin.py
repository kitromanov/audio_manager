from django.contrib import admin
from taggit.models import Tag

from .models import AudioMessage, Comment

admin.site.register(AudioMessage)
admin.site.register(Comment)
