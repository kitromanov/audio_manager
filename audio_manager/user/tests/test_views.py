import json

from django.urls import reverse
from rest_framework import status

from tests_settings.test_setup import CommonTestSetUp
from user.models import User


class TestView(CommonTestSetUp):

    def test_get_all_users(self):
        self.get_authorized_user()
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_blocked_users(self):
        stuff_user = self.get_authorized_user()
        stuff_user.is_staff = True
        stuff_user.save()

        user_data = self.generate_user_data()
        self.register_user(user_data)
        response = self.client.get(reverse('user-blocked'))
        blocked_users = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(all(user['is_blocked'] for user in blocked_users), True)
