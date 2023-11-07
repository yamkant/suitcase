from django.db.models import (
    Model,
    OneToOneField,
    CASCADE
)
from django_celery_results.models import TaskResult

class CeleryTask(Model):
    task_result: OneToOneField = OneToOneField(TaskResult, on_delete=CASCADE)

    class Meta:
        managed = True
        db_table = 'celery_tasks'