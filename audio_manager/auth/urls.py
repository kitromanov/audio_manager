from django.urls import path

from auth.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('email-verify/', EmailVerify.as_view(), name='email_verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request_reset_email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password_reset_complete')
]