from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)
from products.permissions import IsOwner
from core.classes import S3ImageUploader
from django.conf import settings

from users.constants import UserLevelEnum
from products.constants import ProductStatusEnum

from products.tasks import upload_image_by_image_url

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
    lookup_field = "id"

    serializer_action_classes = {
        'list': ProductSerializer,
        'create': ProductCreateSerializer,
        'update': ProductUpdateSerializer,
        'destroy': ProductDeleteSerializer,
    }

    def get_queryset(self):
        return Product.objects.filter(is_deleted="N")

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    def create(self, request, *args, **kwargs):
        if request.user.level == UserLevelEnum.TESTER.value:
            return super().create(request, *args, **kwargs)

        # NOTE: Celery를 사용한 Image Upload 작업
        filename = S3ImageUploader.get_file_name(request.user.username)
        upload_image_by_image_url.delay(request.data['image_url'], filename)

        request.POST._mutable = True
        request.data['saved_image_url'] = f'https://{getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)}/{filename}'
        request.data['user_id'] = request.user.id

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # NOTE: request.POST는 QueryDict 형태로, request.data는 Dict 형태로 반환합니다.
        request.POST._mutable = True
        request.data['is_deleted'] = ProductStatusEnum.DELETED.value
        return super().update(request, *args, **kwargs)