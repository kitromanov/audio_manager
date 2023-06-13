from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action

from user.models import User
from user.serializer import UserSerializer

from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(id=self.request.user.id)

    @action(methods=['get'], detail=False)
    @method_decorator(staff_member_required)
    def blocked(self, request):
        unconfirmed_users = self.queryset.filter(is_blocked=True)
        serializer = self.get_serializer(unconfirmed_users, many=True)
        return Response(serializer.data)
