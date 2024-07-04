from .base import *
#
HOST_URL = 'http://localhost:8000'
DEBUG = True
# STATIC
# STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
# STATIC_URL = '/static/'

# MEDIA
# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

CELERY_BROKER_URL =  "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}