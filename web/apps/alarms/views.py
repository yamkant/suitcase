from rest_framework.response import Response
from users.models import User

from rest_framework.generics import RetrieveAPIView
from django_celery_results.models import TaskResult

from django.shortcuts import get_object_or_404

from django_eventstream import send_event
import json

class TaskRetrieveAPIView(RetrieveAPIView):
    queryset = TaskResult.objects.all()
    lookup_field = ['id']

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(TaskResult, id=kwargs['id'])
        task_kwargs = json.loads(instance.task_kwargs)
        send_event(task_kwargs['channel_name'], 'message', {"msg": f"{instance.task_id} Task Finished"})
        return Response({})