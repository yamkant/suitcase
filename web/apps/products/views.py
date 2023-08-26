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
from rest_framework import filters

from client.pagination import ProductPagination
from users.constants import UserLevelEnum
from products.constants import ProductStatusEnum
from products.swagger import PRODUCT_CREATE_EXAMPLES

from products.tasks import upload_image_by_image_url

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted="N")
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    pagination_class = ProductPagination

    serializer_action_classes = {
        'list': ProductSerializer,
        'create': ProductCreateSerializer,
        'update': ProductUpdateSerializer,
        'destroy': ProductDeleteSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    # TODO: 테스터 추가 예정
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=ProductCreateSerializer,
        summary="새로운 상품을 추가합니다.",
        examples=PRODUCT_CREATE_EXAMPLES,
        responses={
            201: ProductSerializer,
            403: None
        }
    )
    def create(self, request, *args, **kwargs):
        if request.user.level == UserLevelEnum.TESTER.value:
            return super().create(request, *args, **kwargs)
        
        if not request.data.get('image_url'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

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