from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from taggit.models import Tag

from audio.permissions import IsStaffOrCreatorOrAssignedUser
from audio.serializer import *
from audio.models import *
from django.db.models import Q


@extend_schema_view(
    list=extend_schema(
        summary='Retrieves a list of audio messages',
        description="Retrieves a list of audio messages assigned to or created by the authenticated user. Staff "
                    "users can view all tasks.",
        request=AudioMessageSerializer,
        responses={
            200: AudioMessageSerializer(many=True),
            404: OpenApiResponse(description='Audio message not found.'),
        }
    ),
    retrieve=extend_schema(
        summary="Retrieve a single audio message by ID",
        description="Retrieves a single audio message by ID. The ID is specified in the URL.",
        request=AudioMessageSerializer,
        responses={
            200: AudioMessageSerializer
        }
    ),
    create=extend_schema(
        summary='Create a new instance of audio message',
        description='Create a new instance of audio message with the authenticated user as the creator.',
        request=AudioMessageSerializer,
        responses={
            201: AudioMessageSerializer,
        }
    ),
    destroy=extend_schema(
        summary='Delete an instance of audio message',
        description='Delete an instance of audio message with the given primary key. If the authenticated user is a '
                    'staff member, the instance will be permanently deleted. Otherwise, the instance will be '
                    'soft-deleted by setting its "is_deleted" field to True.',
        request=AudioMessageSerializer,
        responses={
            204: {'description': 'The instance was successfully deleted.'},
            403: {'description': 'The authenticated user is not authorized to delete this instance.'},
            404: {'description': 'The instance with the given primary key was not found.'}
        }
    )
)
@extend_schema(tags=["Audio"])
class AudioMessageViewSet(viewsets.ModelViewSet):
    queryset = AudioMessage.objects.all()
    serializer_class = AudioMessageSerializer

    @staticmethod
    def has_access(user, audio):
        if user.is_staff:
            return True
        elif user == audio.creator or user in audio.assigned_users.all():
            return not audio.is_blocked
        else:
            return False

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff:
            self.perform_destroy(instance)
        else:
            instance.is_deleted = True
            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(Q(assigned_users=self.request.user) | Q(creator=self.request.user),
                                        is_deleted=False)

    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        audio = self.get_object()
        return Response(audio.tags.names())

    @action(detail=True, methods=['post'], url_path='add-tag')
    def add_tag(self, request, pk=None):
        audio = self.get_object()
        tag_name = request.data.get('name')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        audio.tags.add(tag)
        audio.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete-tag')
    def delete_tag(self, request, pk=None):
        audio = self.get_object()
        tag_name = request.data.get('name')
        tag = Tag.objects.get(name=tag_name)
        audio.tags.remove(tag)
        audio.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['put'],
            url_path='delete-tag'
            )
    def edit_tag(self, request, pk=None):
        audio = self.get_object()
        tag_id = request.data.get('id')
        tag_name = request.data.get('name')
        tag = Tag.objects.get(id=tag_id)
        tag.name = tag_name
        tag.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['post'],
            url_path='leave-comment',
            permission_classes=[IsStaffOrCreatorOrAssignedUser]
            )
    def leave_comment(self, request, pk=None, audio_id=None):
        audio = self.get_object()
        text = request.data.get('text')
        user = request.user
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(user=user, audio_message=audio, text=text)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True,
            methods=['get'],
            permission_classes=[IsStaffOrCreatorOrAssignedUser]
            )
    def comments(self, request, pk=None):
        comments = Comment.objects.filter(audio_message_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'],
            url_path='delete-comment',
            permission_classes=[IsStaffOrCreatorOrAssignedUser]
            )
    def delete_comment(self, request, pk=None, audio_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(pk=request.data.get('comment_id'))
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
