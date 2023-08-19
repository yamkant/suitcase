from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductCreateSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    serializer_action_classes = {
        'list': ProductSerializer,
        'create': ProductCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    def create(self, request, *args, **kwargs):
        # TODO: url 작업 => 원본 url 배경제거 후 file url을 따로 관리
        return super().create(request, *args, **kwargs)
