from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from audio.audiomessage_serializer import *
from audio.models import *


class AudioMessageViewSet(viewsets.ModelViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
