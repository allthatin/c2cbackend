from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config_secret_common['test']['db']['name'],
        'USER': config_secret_common['test']['db']['user'],
        'PASSWORD': config_secret_common['test']['db']['password'],
        'HOST': config_secret_common['test']['db']['host'],
        'PORT': '5432',
    }
}

DEBUG = False

ALLOWED_HOSTS = ['nallanalla.me', '127.0.0.1', 'test.nallanalla.me']

INSTALLED_APPS += ['storages']

AWS_PRELOAD_METADATA = True
AWS_ACCESS_KEY_ID = config_secret_common['S3']['key']
AWS_SECRET_ACCESS_KEY = config_secret_common['S3']['secret']
AWS_STORAGE_BUCKET_NAME = 'nallanalla.me'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'