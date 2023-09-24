"""
ASGI config for signalserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import re_path, path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_eventstream as django_eventstream

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter({
    'http': URLRouter([
        path('events/<channel>/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), name="eventstream"),
        re_path(r'', get_asgi_application()),
    ]),
})
