from faker import Faker
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APITestCase
from django.urls import reverse

from user.models import User


class CommonTestSetUp(APITestCase):

    def generate_user_data(self):
        password = self.fake.email()
        data = {
            'email': self.fake.email(),
            'username': self.fake.email().split('@')[0],
            'password': password,
            'password2': password,
        }

        return data

    def generate_audio_message_data(self, user_pk, file_path=None):
        if not file_path:
            file_path = 'audio/tests/test_audio1.mp3'
        audio_message_data = {
            'creator': user_pk,
            'incoming_number': self.fake.phone_number()[:20],
            'outgoing_number': self.fake.phone_number()[:20],
            'audio_file': open(file_path, 'rb')
        }
        return audio_message_data

    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('login-view')
        self.reset_password_url = reverse('request_reset_email')

        self.fake = Faker()
        self.user_data = self.generate_user_data()

        return super().setUp()

    def register_user(self, data=None):
        if data:
            return self.client.post(self.register_url, data, format='json')
        else:
            return self.client.post(self.register_url, self.user_data, format='json')

    def login_user(self):
        return self.client.post(self.login_url, self.user_data, format='json')

    @staticmethod
    def verify_email(email):
        user = User.objects.get(email=email)
        user.is_confirmed = True
        return user.save()

    @staticmethod
    def admin_confirmation(email):
        user = User.objects.get(email=email)
        user.is_blocked = False
        return user.save()

    def reg_and_login_user(self, user_data=None):
        register_res = self.register_user(user_data)
        self.verify_email(register_res.data['email'])
        self.admin_confirmation(register_res.data['email'])

        login_res = self.login_user()
        return login_res

    @staticmethod
    def get_access_token_from_login_res(login_res):
        return login_res.data['tokens'].split('\'')[-2]

    def get_authorized_user(self):
        login_res = self.reg_and_login_user()
        token = self.get_access_token_from_login_res(login_res)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        return User.objects.get(email=login_res.data['email'])

    def tearDown(self):
        return super().tearDown()
