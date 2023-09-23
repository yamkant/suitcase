from django.db import models
from django_celery_results.models import TaskResult

class CeleryTask(models.Model):
    task_result = models.OneToOneField(TaskResult, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'celery_tasks'