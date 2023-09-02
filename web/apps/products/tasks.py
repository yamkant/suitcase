from celery import shared_task
from core.classes import ImageHandler, S3ImageUploader
from products.serializers import (
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)
from products.models import Product
from django.shortcuts import get_object_or_404
from celery import chain, group
from django_celery_results.models import TaskResult
from celery.result import AsyncResult
from json import dumps


@shared_task(name='Upload image from url to S3')
def upload_image_by_image_url(img_url, file_path):
    image_handler = ImageHandler(img_url)
    removed_bg_img = image_handler.get_removed_background_image()

    imgUploader = S3ImageUploader()
    saved_image_url = imgUploader.upload_pil(removed_bg_img, file_path)
    return saved_image_url

@shared_task
def async_create_product( data, *args, **kwargs):
    serializer = ProductCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

# NOTE: ignore_result=True 옵션 @shared_task에 추가시 동작 저장 안됨
@shared_task(
    name='Product is_active status bulk update',
    bind=True,
    max_retries=5,
    ignore_result=True
)
def async_bulk_update_product(self, data, *args, **kwargs):
    instance = get_object_or_404(Product, id=kwargs['id'], user_id=kwargs['user_id'])
    serializer = ProductUpdateSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # NOTE: Overhead가 들 수 있기 때문에 적절히 사용할 것
    task = TaskResult.objects.get_task(self.request.id)
    task.task_args = args
    task.task_kwargs = dumps(kwargs)
    task.task_name = self.request.task
    task.worker = self.request.hostname
    task.save()
    return serializer.data

@shared_task(name='Product bulk soft delete')
def async_bulk_delete_product(*args, **kwargs):
    instance = get_object_or_404(Product, id=kwargs['id'], user_id=kwargs['user_id'])
    serializer = ProductDeleteSerializer(instance, data={'is_deleted': 'Y'}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data