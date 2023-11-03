from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault
)
from core.serializers import ReperesntationSerializerMixin

from products.models import Product
from products.constants import ProductDeleteEnum
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

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