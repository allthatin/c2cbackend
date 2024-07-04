import os

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    file_overwrite = False
