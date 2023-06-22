from tests_settings.test_setup import CommonTestSetUp
from user.models import User


class TestView(CommonTestSetUp):
    def test_user_can_register_correctly(self):
        res = self.register_user()
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        login_res = self.reg_and_login_user()
        self.assertEqual(login_res.status_code, 200)

    def test_request_password_reset_email_sends_email_on_existing_user(self):
        self.register_user()
        res = self.client.post(self.reset_password_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', res.data)