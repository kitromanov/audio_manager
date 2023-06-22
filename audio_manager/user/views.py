from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from user.models import User
from user.serializer import UserSerializer

from rest_framework.response import Response


@extend_schema(tags=["User"])
@extend_schema_view(
    list=extend_schema(
        summary='Returns a List all users',
        description='Returns a List all users or filter by id if not staff',
        responses={
            200: UserSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary='Retrieve user',
        description='Retrieve a specific user by ID',
        responses={
            200: UserSerializer(),
        },
    ),
    create=extend_schema(
        summary='Create user',
        description='Create a new user',
        request=UserSerializer(),
        responses={
            201: UserSerializer(),
        },
    ),
    destroy=extend_schema(
        summary='Delete an instance of user',
        description='Delete an instance of user with the given primary key.',
        request=UserSerializer(),
        responses={
            204: {'description': 'The instance was successfully deleted.'},
            403: {'description': 'The authenticated user is not authorized to delete this instance.'},
            404: {'description': 'The instance with the given primary key was not found.'}
        }
    ),
    update=extend_schema(
        summary='Update user',
        description='Update an existing user by ID',
        request=UserSerializer(),
        responses={
            200: UserSerializer(),
        },
    ),
    partial_update=extend_schema(
        summary='Partial update user',
        description='Partially update an existing user by ID',
        request=UserSerializer(),
        responses={
            200: UserSerializer(),
        },
    ),
    blocked=extend_schema(
        summary='List blocked users',
        description='List all blocked users in the system',
        responses={
            200: UserSerializer(many=True),
        },
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(id=self.request.user.id)

    @extend_schema(
        description="List all blocked users",
        parameters=[OpenApiParameter(name="is_blocked", type=bool, location=OpenApiParameter.QUERY,
                                     description="Filter by blocked status")],
        responses={200: UserSerializer(many=True)}
    )
    @action(methods=['get'], detail=False)
    @method_decorator(staff_member_required)
    def blocked(self, request):
        unconfirmed_users = self.queryset.filter(is_blocked=True)
        serializer = self.get_serializer(unconfirmed_users, many=True)
        return Response(serializer.data)
