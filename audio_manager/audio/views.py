from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audio.audiomessage_serializer import *
from audio.models import *


class AudioMessageViewSet(viewsets.ModelViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
