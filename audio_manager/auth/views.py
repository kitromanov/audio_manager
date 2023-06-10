import jwt
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from auth.serializers import RegisterSerializer, LoginSerializer
from user.models import User
from .renderers import UserRenderer
from .util import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.conf import settings

import os
from dotenv import load_dotenv

load_dotenv()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    # permission_classes = (AllowAny,)
    # serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
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


class EmailVerify(generics.GenericAPIView):
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
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
