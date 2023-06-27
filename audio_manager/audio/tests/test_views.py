from rest_framework import status
from rest_framework.reverse import reverse

from audio.models import AudioMessage
from tests_settings.test_setup import CommonTestSetUp


class TestView(CommonTestSetUp):

    def test_create_audio_message(self):
        user = self.get_authorized_user()
        user.is_staff = True
        user.save()
        audio_message_data = self.generate_audio_message_data(user.pk)
        response = self.client.post(reverse('audio-message-list'), audio_message_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_tag(self):
        user = self.get_authorized_user()
        audio_message_data = self.generate_audio_message_data(user.pk)
        response = self.client.post(reverse('audio-message-list'), audio_message_data)
        audio_message = AudioMessage.objects.get(pk=response.data['id'])
        url = reverse('audio-message-add-tag', kwargs={'pk': response.data['id']})
        tag_data = {'name': 'test_tag'}
        response = self.client.post(url, tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(audio_message.tags.all()), 1)

    def test_add_comment(self):
        user = self.get_authorized_user()
        audio_message_data = self.generate_audio_message_data(user.pk)
        response = self.client.post(reverse('audio-message-list'), audio_message_data)
        audio_message = AudioMessage.objects.get(pk=response.data['id'])
        url = reverse('audio-message-leave-comment', kwargs={'pk': response.data['id']})
        comment_data = {'text': 'test_comment'}
        response = self.client.post(url, comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(audio_message.comments_audio_message.all()), 1)