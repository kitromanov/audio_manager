from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.forms import SignupForm
from auth.tokens import account_activation_token
from user.models import User
from django.contrib import auth
from .util import Util
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):

        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        print(user)
        if not user.is_confirmed:
            raise AuthenticationFailed('Email is not verified.')
        if user.is_blocked:
            raise AuthenticationFailed('Account disabled, contact admin.')
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
        }

        return super().validate(attrs)
        # credentials = {
        #     'username': '',
        #     'password': attrs.get("password")
        # }
        #
        # email_address = attrs.get("email")
        # is_confirmed = User.objects.get(email=attrs.get("email")).is_confirmed
        #
        # if email_address and is_confirmed:
        #     credentials['email'] = email_address
        #     return super().validate(credentials)
        # elif email_address and not is_confirmed:
        #     return {'message': 'Email not verified'}
        # else:
        #     return {'message': 'This email does not exist, please create a new account'}

    # @classmethod
    # def get_token(cls, user):
    #     token = super(MyTokenObtainPairSerializer, cls).get_token(user)
    #
    #     token['username'] = user.username
    #
    #     return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.save()
        return user

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#
#         token['username'] = user.username
#
#         return token
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_confirmed = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})
