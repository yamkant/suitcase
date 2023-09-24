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
from products.swagger import (
    PRODUCT_CREATE_EXAMPLES,
    PRODUCT_LIST_EXAMPLES,
    PRODUCT_UPDATE_EXAMPLES,
)

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.core.cache import cache
from client.libs.cache import get_cache_product_count_key

from products.tasks import (
    upload_image_by_image_url,
    async_bulk_update_product,
    async_bulk_delete_product,
)

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
    @extend_schema(
        request=ProductSerializer,
        summary="상품 목록을 조회합니다.",
        description="""상품 목록을 페이지번호/페이지크기/검색결과에 따라 조회합니다.""",
        tags=['상품'],
        parameters=PRODUCT_LIST_EXAMPLES,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
    
    @extend_schema(
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
    def create(self, request, *args, **kwargs):
        if request.user.level == UserLevelEnum.TESTER.value:
            return super().create(request, *args, **kwargs)
        
        if not request.data.get('image_url'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # NOTE: Celery를 사용한 Image Upload 작업
        filename = S3ImageUploader.get_file_name(request.user.username)
        data = {
            'img_url': request.data['image_url'],
            'file_path': filename,
        }
        upload_image_by_image_url.delay(
            data=data,
            user_id=request.user.id,
        )

        request.POST._mutable = True
        request.data['saved_image_url'] = f'https://{getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)}/{filename}'
        request.data['user_id'] = request.user.id

        cache.delete(get_cache_product_count_key(request.user.id))

        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ProductUpdateSerializer,
        summary="상품을 활성화/비활성화 및 정보들을 수정합니다.",
        description="""'Edit product' modal에서 상품의 이름, 카테고리와 같은 기본적인 정보를 수정합니다.<br>is_active 필드의 활성여부에 따라 Fitting 페이지에서 상품을 사용여부가 결정됩니다.""",
        tags=['상품'],
        examples=PRODUCT_UPDATE_EXAMPLES,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_403_FORBIDDEN: None
        }
    )
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
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
    def destroy(self, request, *args, **kwargs):
        # NOTE: request.POST는 QueryDict 형태로, request.data는 Dict 형태로 반환합니다.
        request.POST._mutable = True
        request.data['is_deleted'] = ProductStatusEnum.DELETED.value
        cache.delete(get_cache_product_count_key(request.user.id))
        return super().update(request, *args, **kwargs)

class ProductBulkViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted="N")
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]

    def bulk_update(self, request, *args, **kwargs):
        if 'prod_list[]' not in request.data:
            return Response({})
        prod_id_list = request.data.getlist('prod_list[]')
        data = {
            'is_active': request.data['is_active'],
        }
        for prod_id in prod_id_list:
            task = async_bulk_update_product.delay(
                data=data, 
                id=prod_id,
                user_id=request.user.id,
            )
        return Response({})

    def bulk_delete(self, request, *args, **kwargs):
        if 'prod_list[]' not in request.data:
            return Response({})
        # NOTE: user가 가지고있는 product가 맞는지 확인
        prod_id_list = request.data.getlist('prod_list[]')
        for prod_id in prod_id_list:
            async_bulk_delete_product.delay(
                id=prod_id,
                user_id=request.user.id,
            )
        return Response({})