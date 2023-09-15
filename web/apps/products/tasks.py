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

from config.serializers import TaskResultUpdateSerializer
from celery import states
from products.constants import ProductAlarmStatusEnum

# TODO: upload 문제 발생시 is_uploaded 값 'E'로 수정
@shared_task(name='Update product status')
def update_product_status(saved_img_url):
    instance = get_object_or_404(Product, saved_image_url=saved_img_url)
    serializer = ProductUpdateSerializer(instance, data={
        'is_uploaded': ProductAlarmStatusEnum.UPLOADED.value,
    }, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return True


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

def update_task_results(task_id, data):
    task = TaskResult.objects.get_task(task_id)
    task_serializer = TaskResultUpdateSerializer(task, data=data, partial=True)
    task_serializer.is_valid(raise_exception=True)
    task_serializer.save()
    return task_serializer.data

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

    update_task_results(task_id=self.request.id, data={
        'task_name': self.request.task,
        'task_args': dumps(args),
        'task_kwargs': dumps(kwargs),
        'worker': self.request.hostname,
        'status': states.SUCCESS
    })
    # NOTE: Overhead가 들 수 있기 때문에 적절히 사용할 것
    return serializer.data

@shared_task(
    name='Product bulk soft delete',
    bind=True,
    max_retries=5,
    ignore_result=True
)
def async_bulk_delete_product(self, *args, **kwargs):
    instance = get_object_or_404(Product, id=kwargs['id'], user_id=kwargs['user_id'])
    serializer = ProductDeleteSerializer(instance, data={'is_deleted': 'Y'}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    update_task_results(task_id=self.request.id, data={
        'task_name': self.request.task,
        'task_args': dumps(args),
        'task_kwargs': dumps(kwargs),
        'worker': self.request.hostname,
        'status': states.SUCCESS
    })
    return serializer.data

import time
@shared_task()
def test_task(self, *args, **kwargs):
    time.sleep(5)
    print("task finished")
    return "hihi"