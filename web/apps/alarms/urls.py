from django.urls import path
from django.conf.urls import include
import django_eventstream
from alarms.views import TaskRetrieveAPIView

urlpatterns = [
    path('events/<channel>/', include(django_eventstream.urls)),
    path("tasks/<int:id>/", TaskRetrieveAPIView.as_view(), name="task-detail"),
]