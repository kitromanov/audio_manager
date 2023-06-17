import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny

from auth.serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer, \
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from user.models import User
from .renderers import UserRenderer
from .util import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.conf import settings
from drf_yasg import openapi

import os
from dotenv import load_dotenv

load_dotenv()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    permission_classes = (AllowAny,)

    def post(self, request):
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

    @staticmethod
    def get(request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_confirmed:
                user.is_confirmed = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            relative_link = reverse('password_reset_confirm', kwargs={
                'uidb64': uidb64,
                'token': token
            })
            abs_url = os.getenv("HOST_NAME") + relative_link + '?token=' + str(token)
            data = {
                'email_body': 'Hi, ' + user.username + '! Use link below to reset you password.\n\n' + abs_url,
                'domain': abs_url,
                'email_subject': 'Reset your password',
                'to_email': (user.email,),
            }
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    @staticmethod
    def get(request, uidb64, token):

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
