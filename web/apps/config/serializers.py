from rest_framework.serializers import ModelSerializer
from django_celery_results.models import TaskResult
from core.serializers import UpdateSerializer

class TaskResultSerializer(ModelSerializer):
    class Meta:
        model = TaskResult
        fields = (
            "task_id",
            "task_name",
            "task_args",
            "task_kwargs",
            "status",
        )
        read_only_fields = fields

class TaskResultUpdateSerializer(UpdateSerializer):
    representation_serializer_class = TaskResultSerializer

    class Meta:
        model = TaskResult
        fields = (
            "task_name",
            "task_args",
            "task_kwargs",
            "status",
            "worker",
        )

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
