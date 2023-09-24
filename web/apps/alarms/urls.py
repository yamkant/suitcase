from django.urls import path
from django.conf.urls import include
import django_eventstream
from rest_framework.response import Response
from users.models import User

from rest_framework.generics import RetrieveAPIView
from django_celery_results.models import TaskResult

from django.shortcuts import get_object_or_404

from django_eventstream import send_event
import json

class TaskAPIView(RetrieveAPIView):
    queryset = TaskResult.objects.all()
    lookup_field = ['id']
    # renderer_classes = [JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(TaskResult, id=kwargs['id'])
        task_data = json.loads(instance.task_kwargs)
        user = get_object_or_404(User, id=task_data['user_id'])
        send_event(user.username, 'message', {"msg": f"{instance.task_id} Task Finished"})
        return Response({})

urlpatterns = [
    path('events/<channel>/', include(django_eventstream.urls)),
    path("tasks/<int:id>/", TaskAPIView.as_view(), name="task-detail"),
]