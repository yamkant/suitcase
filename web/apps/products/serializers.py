
from rest_framework import serializers
from core.serializers import CreateSerializer, UpdateSerializer

from products.models import Product
from users.models import User
from django.shortcuts import get_object_or_404

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "image_url",
            "is_favorite",
            "is_profile",
            "user_id",
        )
        read_only_fields = fields

class ProductCreateSerializer(CreateSerializer):
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "name",
            "image_url",
            "user_id",
        )
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        validated_data['user_id'] = get_object_or_404(User, id=validated_data['user_id'])
        return Product.objects.create(**validated_data)