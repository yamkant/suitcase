from rest_framework import serializers
from core.serializers import CreateSerializer, UpdateSerializer

from products.models import Product
from products.constants import ProductStatusEnum, ProductDeleteEnum
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator


class ProductSerializer(serializers.ModelSerializer):

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

class ProductCreateSerializer(CreateSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class ProductUpdateSerializer(UpdateSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "is_active",
            "user_id",
        )
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ProductDeleteSerializer(UpdateSerializer):
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "is_deleted",
        )
    
    def update(self, instance, validated_data):
        instance.is_deleted = ProductDeleteEnum.DELETED.value
        return super().update(instance, validated_data)