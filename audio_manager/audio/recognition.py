import boto3
import requests
import time


class RecognitionLongAudio:
    ENDPOINT = 'https://storage.yandexcloud.net'
    BASE_FILE_LINK = 'https://storage.yandexcloud.net/'

    def __init__(self, api_key, bucket_name):
        self.api_key = api_key
        self.bucket_name = bucket_name
        session = boto3.session.Session()
        self.s3 = s3 = session.client(
            service_name='s3',
            endpoint_url=self.ENDPOINT,
        )

    def create_bucket(self, name):
        r = self.s3.create_bucket(Bucket=name)

    def upload_to_bucket(self, path, file_name):
        self.s3.upload_file(r"{}".format(path + file_name), self.bucket_name, file_name)

    def recognize(self, file_name):
        file_link = self.BASE_FILE_LINK + self.bucket_name + '/' + file_name
        file_type = 'MP3' if file_name.endswith('mp3') else 'OGG_OPUS'
        post_req = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
        body = {
            "config": {
                "specification": {
                    "languageCode": "ru-RU",
                    "model": "deferred-general",
                    'audioEncoding': file_type
                }
            },
            "audio": {
                "uri": file_link
            }
        }
        header = {'Authorization': 'Api-Key {}'.format(self.api_key)}
        req = requests.post(post_req, headers=header, json=body)
        data = req.json()
        return [data['id'], header]

    @staticmethod
    def get_text_transcription(data_id, header):
        step = 10
        while True:
            time.sleep(step)
            get_req = "https://operation.api.cloud.yandex.net/operations/{id}"
            req = requests.get(get_req.format(id=data_id), headers=header)
            req = req.json()
            if req['done']:
                break
        transcription = ''
        for chunk in req['response']['chunks']:
            transcription += chunk['alternatives'][0]['text']
        return transcription
