from rest_framework.serializers import (
    BaseSerializer,
    ModelSerializer
)

class CreateSerializer(ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data

class UpdateSerializer(ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data

class ReperesntationSerializerMixin(BaseSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data