from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audio.audiomessage_serializer import *
from audio.models import *


class AudioMessageViewSet(viewsets.ModelViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AudioMessageSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def patch(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = TagSerializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)