from celery import Celery

app = Celery('audio_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
