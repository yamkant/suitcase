from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers.products import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)
from products.permissions import IsOwner
from core.classes import S3ImageUploader
from django.conf import settings
from rest_framework import filters

from products.pagination import ProductPagination
from users.constants import UserLevelEnum
from products.constants import ProductStatusEnum, ProductDeleteEnum
from products.swagger import (
    PRODUCT_CREATE_EXAMPLES,
    PRODUCT_LIST_EXAMPLES,
    PRODUCT_UPDATE_EXAMPLES,
)

from drf_spectacular.utils import extend_schema, extend_schema_view
from django.core.cache import cache
from client.libs.cache import get_cache_product_count_key

from products.tasks import (
    upload_image_by_image_url,
)
from django_eventstream import send_event

@extend_schema_view(
    get=extend_schema(
        request=ProductSerializer,
        summary="상품 목록을 조회합니다.",
        description="""상품 목록을 페이지번호/페이지크기/검색결과에 따라 조회합니다.""",
        tags=['상품'],
        parameters=PRODUCT_LIST_EXAMPLES,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    ),
    post=extend_schema(
        request=ProductCreateSerializer,
        summary="새로운 상품을 추가합니다.",
        description="""'Add product' modal에서 상품을 등록하는 예시입니다. 상품의 이미지 주소와 이름을 입력하면 비동기작업으로 업로드가 수행됩니다.""",
        tags=['상품'],
        examples=PRODUCT_CREATE_EXAMPLES,
        responses={
            status.HTTP_201_CREATED: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    )
)
class ProductListView(ListCreateAPIView):
    queryset = Product.active_objects.order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    pagination_class = ProductPagination

    serializer_action_classes = {
        'GET': ProductSerializer,
        'POST': ProductCreateSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.request.method]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    def create(self, request, *args, **kwargs):
        if not request.data.get('image_url'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # NOTE: Celery를 사용한 Image Upload 작업
        filename = S3ImageUploader.get_file_name(request.user.username)
        data = {
            'img_url': request.data.get('image_url'),
            'file_path': filename,
            'channel_name': request.user.username,
        }
        
        if request.user.level != UserLevelEnum.TESTER.value:
            upload_image_by_image_url.delay(**data)
        request.POST._mutable = True
        request.data['saved_image_url'] = f'https://{getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)}/{filename}'

        cache.delete(get_cache_product_count_key(request.user.id))
        return super().create(request, *args, **kwargs)

@extend_schema_view(
    patch=extend_schema(
        request=ProductUpdateSerializer,
        summary="상품을 활성화/비활성화 및 정보들을 수정합니다.",
        description="""'Edit product' modal에서 상품의 이름, 카테고리와 같은 기본적인 정보를 수정합니다.<br>is_active 필드의 활성여부에 따라 Fitting 페이지에서 상품을 사용여부가 결정됩니다.""",
        tags=['상품'],
        examples=PRODUCT_UPDATE_EXAMPLES,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    ),
    delete=extend_schema(
        request=ProductUpdateSerializer,
        summary="상품을 제거(논리적 제거)합니다.",
        tags=['상품'],
        description="""상품테이블에서 is_deleted의 필드값을 'Y'로 수정하여, 유저에게는 제거된 것처럼 보이게 합니다.""",
        examples=PRODUCT_UPDATE_EXAMPLES,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    )
)
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.active_objects.order_by('-created_at')
    lookup_field = "id"
    serializer_action_classes = {
        'PATCH': ProductUpdateSerializer,
        'DELETE': ProductDeleteSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.request.method]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    def delete(self, request, *args, **kwargs):
        cache.delete(get_cache_product_count_key(request.user.id))
        return super().update(request, *args, **kwargs)

class ProductBulkViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Product.active_objects
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        if 'prod_list' not in request.data:
            return Response({})
        prod_id_list = request.data.get('prod_list')
        if request.data.get('is_active') not in [
            ProductStatusEnum.ACTIVE.value,
            ProductStatusEnum.DEACTIVE.value,
        ]:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        Product.active_objects.get_in_list(prod_id_list).filter(user_id=request.user.id).update(is_active=request.data.get('is_active'))
        send_event(request.user.username, 'message', {"type": f"edit"})
        return Response({})

    def delete(self, request, *args, **kwargs):
        if 'prod_list' not in request.data:
            return Response({})
        prod_id_list = request.data.get('prod_list')
        Product.active_objects.get_in_list(prod_id_list).filter(user_id=request.user.id).update(is_deleted=ProductDeleteEnum.DELETED.value)
        send_event(request.user.username, 'message', {"type": f"edit"})
        return Response({})