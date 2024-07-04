"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os

# import django
# from.wsgi import *
# from channels.auth import AuthMiddlewareStack
# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter, URLRouter


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
# django.setup()

# application = ProtocolTypeRouter({
#     "http": AsgiHandler(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })