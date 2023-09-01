from celery import shared_task
from core.classes import ImageHandler, S3ImageUploader
from products.serializers import (
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)
from products.models import Product
from django.shortcuts import get_object_or_404


@shared_task
def upload_image_by_image_url(img_url, file_path):
    image_handler = ImageHandler(img_url)
    removed_bg_img = image_handler.get_removed_background_image()

    imgUploader = S3ImageUploader()
    saved_image_url = imgUploader.upload_pil(removed_bg_img, file_path)
    return saved_image_url

@shared_task
def async_create_product(data, *args, **kwargs):
    serializer = ProductCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

@shared_task
def async_bulk_update_product(data, *args, **kwargs):
    instance = get_object_or_404(Product, id=kwargs['id'], user_id=kwargs['user_id'])
    serializer = ProductUpdateSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

@shared_task
def async_bulk_delete_product(*args, **kwargs):
    instance = get_object_or_404(Product, id=kwargs['id'], user_id=kwargs['user_id'])
    serializer = ProductDeleteSerializer(instance, data={'is_deleted': 'Y'}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data