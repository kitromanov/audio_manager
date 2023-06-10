from rest_framework import viewsets
from rest_framework.response import Response

from audio.serializer import *
from audio.models import *
from django.db.models import Q


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

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(Q(assigned_users=self.request.user) | Q(creator=self.request.user))


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
