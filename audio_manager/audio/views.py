from rest_framework import viewsets
from rest_framework.response import Response

from audio.serializer import *
from audio.models import *


class BaseViewSet(viewsets.ModelViewSet):
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AudioMessageViewSet(BaseViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
