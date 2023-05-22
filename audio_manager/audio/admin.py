from django.contrib import admin
from .models import AudioMessage, Tag, Comment

admin.site.register(AudioMessage)
admin.site.register(Tag)
admin.site.register(Comment)
