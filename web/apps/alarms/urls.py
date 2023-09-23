from django.urls import path
from django.conf.urls import include
import django_eventstream
from rest_framework.response import Response

from rest_framework.generics import RetrieveAPIView
from django_celery_results.models import TaskResult

from django.shortcuts import get_object_or_404

from django_eventstream import send_event

class TaskAPIView(RetrieveAPIView):
    queryset = TaskResult.objects.all()
    lookup_field = ['id']
    # renderer_classes = [JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(TaskResult, id=kwargs['id'])
        send_event('testchannel', 'message', {"msg": f"{instance.task_id} Task Finished"})
        # return super().retrieve(request, *args, **kwargs)
        return Response({})

urlpatterns = [
    path('events/', include(django_eventstream.urls), {
        'channels': ['testchannel']
    }),
    path("tasks/<int:id>/", TaskAPIView.as_view(), name="task-detail"),
]