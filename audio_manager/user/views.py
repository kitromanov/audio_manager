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
# @extend_schema_view(
#     list=swagger_auto_schema(
#         operation_summary='List users',
#         operation_description='List all users in the system',
#         responses={
#             200: UserSerializer(many=True),
#             401: 'Unauthorized',
#         },
#     ),
#     retrieve=swagger_auto_schema(
#         operation_summary='Retrieve user',
#         operation_description='Retrieve a specific user by ID',
#         responses={
#             200: UserSerializer(),
#             401: 'Unauthorized',
#             404: 'Not found',
#         },
#     ),
#     create=swagger_auto_schema(
#         operation_summary='Create user',
#         operation_description='Create a new user',
#         request_body=UserSerializer(),
#         responses={
#             201: UserSerializer(),
#             401: 'Unauthorized',
#             400: 'Bad request',
#         },
#     ),
#     update=swagger_auto_schema(
#         operation_summary='Update user',
#         operation_description='Update an existing user by ID',
#         request_body=UserSerializer(),
#         responses={
#             200: UserSerializer(),
#             401: 'Unauthorized',
#             400: 'Bad request',
#             404: 'Not found',
#         },
#     ),
#     partial_update=swagger_auto_schema(
#         operation_summary='Partial update user',
#         operation_description='Partially update an existing user by ID',
#         request_body=UserSerializer(),
#         responses={
#             200: UserSerializer(),
#             401: 'Unauthorized',
#             400: 'Bad request',
#             404: 'Not found',
#         },
#         security=[],
#     ),
#     blocked=swagger_auto_schema(
#         operation_summary='List blocked users',
#         operation_description='List all blocked users in the system',
#         responses={
#             200: UserSerializer(many=True),
#             401: 'Unauthorized',
#             403: 'Forbidden',
#         },
#         security=[{'Bearer': []}],
#     ),
# )
# @extend_schema(
#     description="A viewset for users",
#     responses={
#         200: UserSerializer(many=True),
#         403: OpenApiResponse(description="Forbidden"),
#     },
# )
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        description="List all users or filter by id if not staff",
        responses={
            200: OpenApiResponse(response=UserSerializer(many=True), description="OK"),
            500: OpenApiResponse(description="Server error")
        }
    )
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
