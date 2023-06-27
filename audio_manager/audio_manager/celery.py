import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_manager.settings')
app = Celery('audio_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
