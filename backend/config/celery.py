from __future__ import absolute_import, unicode_literals
import os
import logging

from celery import Celery
from celery.signals import setup_logging

logger = logging.getLogger()

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery(broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings')

# ## Celery에 Django Logging 모듈 적용
@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)

app.autodiscover_tasks(settings.INSTALLED_APPS)
