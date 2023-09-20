import os
from celery import Celery
from core import settings
# from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# config('DJANGO_SETTINGS_MODULE', default='core.settings')

# Cria uma instância do Celery
app = Celery(
    'core',
    broker=settings.CELERY_BROKER_URL,
    # backend=settings.CELERY_RESULT_BACKEND,  # Descomente esta linha se desejar um backend
)
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
