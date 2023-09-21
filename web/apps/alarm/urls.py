from django.urls import path
from django.conf.urls import include
import django_eventstream


urlpatterns = [
    path('events/', include(django_eventstream.urls), {
        'channels': ['testchannel']
    }),
]