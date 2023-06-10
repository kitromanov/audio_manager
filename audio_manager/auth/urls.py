from django.urls import path

from auth.views import *
# from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('email-verify/', EmailVerify.as_view(), name='email_verify'),
]