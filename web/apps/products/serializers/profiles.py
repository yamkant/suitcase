from rest_framework import serializers
from core.serializers import CreateSerializer, UpdateSerializer
from products.models import ProductProfile

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductProfile
        fields = (
            "id",
            "prod_id",
            "category",
        )
        read_only_fields = fields

class ProductProfileCreateSerializer(CreateSerializer):
    representation_serializer_class = ProductSerializer

    class Meta:
        model = ProductProfile
        fields = (
            "id",
            "prod_id",
            "category",
        )