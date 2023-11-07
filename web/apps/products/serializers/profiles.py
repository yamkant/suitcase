from rest_framework.serializers import (
    ModelSerializer
)

from core.serializers import ReperesntationSerializerMixin
from products.models import ProductProfile

class ProductSerializer(ModelSerializer):

    class Meta:
        model = ProductProfile
        fields = (
            "id",
            "prod_id",
            "category",
        )
        read_only_fields = fields

class ProductProfileCreateSerializer(ReperesntationSerializerMixin, ModelSerializer):
    representation_serializer_class: ModelSerializer = ProductSerializer

    class Meta:
        model = ProductProfile
        fields = (
            "id",
            "prod_id",
            "category",
        )