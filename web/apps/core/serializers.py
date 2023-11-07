from rest_framework.serializers import (
    ModelSerializer
)
from typing import Any, Optional

class CreateSerializer(ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data

class UpdateSerializer(ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data

class ReperesntationSerializerMixin(ModelSerializer):
    representation_serializer_class: Optional[ModelSerializer] = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data