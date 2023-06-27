from celery import shared_task

from audio.recognition import RecognitionLongAudio
import os
from dotenv import load_dotenv

load_dotenv()


@shared_task
def get_audio_text(file_name):
    recognition = RecognitionLongAudio(
        api_key=os.getenv("API_KEY"),
        bucket_name=os.getenv("BUCKET")
    )
    recognition.upload_to_bucket('', file_name)
    result = recognition.recognize(file_name)
    return recognition.get_text_transcription(*result)
