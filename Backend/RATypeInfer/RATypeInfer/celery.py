from celery import Celery
import os

# Load configuration from Django settings or another config file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RATypeInfer.settings')
app = Celery('RATypeInfer')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in registered apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
