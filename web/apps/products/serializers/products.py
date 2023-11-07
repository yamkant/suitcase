from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault
)
from apps.core.serializers import ReperesntationSerializerMixin

from apps.products.models import Product
from apps.products.constants import ProductDeleteEnum

class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "image_url",
            "saved_image_url",
            "is_active",
            "is_deleted",
        )
        read_only_fields = fields

class ProductCreateSerializer(ReperesntationSerializerMixin, ModelSerializer):
    user_id = HiddenField(default=CurrentUserDefault())
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "name",
            "image_url",
            "saved_image_url",
            "category",
            "user_id",
        )

class ProductUpdateSerializer(ReperesntationSerializerMixin, ModelSerializer):
    user_id = HiddenField(default=CurrentUserDefault())
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "is_active",
            "user_id",
        )

class ProductDeleteSerializer(ReperesntationSerializerMixin, ModelSerializer):
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "is_deleted",
        )
    
    def update(self, instance, validated_data):
        instance.is_deleted = ProductDeleteEnum.DELETED.value
        return super().update(instance, validated_data)