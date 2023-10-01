from celery import shared_task
from core.classes import ImageHandler, S3ImageUploader
from products.serializers.products import (
    ProductCreateSerializer,
)
from products.models import Product
from django.shortcuts import get_object_or_404
from celery import chain, group
from django_celery_results.models import TaskResult
from celery.result import AsyncResult
from json import dumps

from config.serializers import TaskResultUpdateSerializer
from celery import states

def update_task_results(task_id, data):
    task = TaskResult.objects.get_task(task_id)
    task_serializer = TaskResultUpdateSerializer(task, data=data, partial=True)
    task_serializer.is_valid(raise_exception=True)
    task_serializer.save()
    return task_serializer.data

@shared_task(
    name='Upload image from url to S3',
    bind=True,
    max_retries=5,
    ignore_result=True
)
def upload_image_by_image_url(self, *args, **kwargs):
    img_url = kwargs.get('img_url')
    file_path = kwargs.get('file_path')
    image_handler = ImageHandler(img_url)
    removed_bg_img = image_handler.get_removed_background_image()

    imgUploader = S3ImageUploader()
    saved_image_url = imgUploader.upload_pil(removed_bg_img, file_path)

    update_task_results(task_id=self.request.id, data={
        'task_name': self.request.task,
        'task_args': dumps(args),
        'task_kwargs': dumps(kwargs),
        'worker': self.request.hostname,
        'status': states.SUCCESS
    })
    return saved_image_url

@shared_task
def async_create_product( data, *args, **kwargs):
    serializer = ProductCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data
