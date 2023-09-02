from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery(
    'config',
    broker_connection_retry_on_startup=True
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.timezone = "Asia/Seoul"
app.conf.task_track_started = True
app.conf.task_time_limit = 30 * 60
app.conf.task_serializer = 'json'



@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
