import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # noqa: T001


app.conf.beat_schedule = {
    'shop_sync': {
        'task': 'shop.tasks.shop_sync',
        'schedule': crontab(minute=0, hour=0)
    }}
