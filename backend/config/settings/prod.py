from .base import *
import sentry_sdk
ENV = "prod"
HOST_URL = 'https://api.nallanalla.com'
DEBUG=False
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': config_secret_common['DB']['HOST'],
#         'NAME': config_secret_common['DB']['NAME'],
#         'USER': config_secret_common['DB']['USER'],
#         'PASSWORD': config_secret_common['DB']['PASSWORD'],
#         'PORT': config_secret_common['DB']['PORT'],
#     }
# }

AWS_LOCATION = 'nallanallamedia/static'
MEDIA_URL = 'nallanallamedia/media/'
MEDIA_LOCATION = 'nallanallamedia/media'

AWS_PRELOAD_METADATA = True
AWS_ACCESS_KEY_ID = config_secret_common['AWS']['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_common['AWS']['aws_secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret_common['S3']['bucket']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# # STATIC
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# MEDIA
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'


if REDIS_HOST:
    CELERY_BROKER_URL = "redis://%s:%s" %(REDIS_HOST,REDIS_PORT)
    CELERY_RESULT_BACKEND = "redis://%s:%s" %(REDIS_HOST,REDIS_PORT)
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_BROKER_CONNECTION_RETRY = True
    CELERY_TIMEZONE = TIME_ZONE

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://%s:%s" %(REDIS_HOST,REDIS_PORT),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
        },
    }
else:
    CACHES = {
        "admin_interface": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "TIMEOUT": 60 * 5,
        },
    }

CRONJOBS = [
    #('*/10 * * * *','django.core.management.call_command',['create_sellresponse'],{},'>> /var/log/create_sellresponse 2>&1'),
    # ('*/2 * * * *','django.core.management.call_command',['request_reservation'],{},'>> /var/log/request_reservation 2>&1'),
    # ('0 * * * *','django.core.management.call_command',['request_remind'],{},'>> /var/log/request_remind 2>&1'),
    
]