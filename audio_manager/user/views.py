from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from user.models import User
from user.serializer import UserSerializer

from rest_framework.response import Response


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return User.objects.all()
        else:
            return User.objects.filter(pk=pk)

    @action(methods=['get'], detail=False)
    def unconfirmed(self, request):
        unconfirmed_users = self.queryset.filter(is_confirmed=False)
        serializer = self.get_serializer(unconfirmed_users, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
