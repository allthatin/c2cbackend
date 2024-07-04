from .base import *
ENV = "dev"

HOST_URL = 'https://api.nallanalla.com'

# # STATIC
# STATIC_DIR = os.path.join(ROOT_DIR, 'static')
# STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
# STATICFILES_DIRS = [
#     os.path.join(ROOT_DIR, 'static'),
# ]
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media
# MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
# MEDIA_URL = 'dev/media/'
# MEDIA_LOCATION = 'dev/media'
# DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'

if REDIS_HOST:
    CELERY_BROKER_URL = "redis://%s:%s" %(REDIS_HOST,REDIS_PORT)
    CELERY_RESULT_BACKEND ="redis://%s:%s" %(REDIS_HOST,REDIS_PORT)
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://%s:%s" %(REDIS_HOST,REDIS_PORT),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
        }
    }
else:
    CACHES = {
        "admin_interface": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "TIMEOUT": 60 * 5,
        },
    }