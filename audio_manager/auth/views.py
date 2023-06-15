import jwt
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny

from auth.serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from user.models import User
from .renderers import UserRenderer
from .util import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import os
from dotenv import load_dotenv

load_dotenv()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    # @extend_schema(
    #     request=LoginSerializer,
    #     responses={status.HTTP_200_OK: LoginSerializer}
    # )
    def post(self, request):
        """
        User login.

        Authenticates the user based on the passed credentials.

        :param request: request object
        :return: response object
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    permission_classes = (AllowAny,)

    # @extend_schema(
    #     request=RegisterSerializer,
    #     responses={status.HTTP_201_CREATED: RegisterSerializer}
    # )
    def post(self, request):
        """
        Register a new user.

        Creates a new user based on the provided data and sends an email for email verification.

        :param request: the request object
        :return: the response object
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        relative_link = str(reverse('email_verify'))
        abs_url = os.getenv("HOST_NAME") + relative_link + '?token=' + str(token)
        data = {
            'email_body': 'Hi, ' + user.username + '! Use link below to verify your email.\n\n' + abs_url,
            'domain': abs_url,
            'email_subject': 'Verify your email',
            'to_email': (user.email,),
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerify(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)

    token_param_config = openapi.Parameter('token',
                                           in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING,
                                           )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    # @extend_schema(
    #     parameters=[token_param_config],
    #     responses={status.HTTP_200_OK: {'email': 'Successfully activated'}}
    # )
    def get(self, request):
        """
        Email confirmation.

        Confirms the user's email based on the passed token.

        :param request: request object
        :return: response object
        """
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_confirmed:
                user.is_confirmed = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
