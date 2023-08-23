from celery import shared_task
from core.classes import ImageHandler, S3ImageUploader


@shared_task
def upload_image_by_image_url(img_url, file_path):
    image_handler = ImageHandler(img_url)
    removed_bg_img = image_handler.get_removed_background_image()
    resized_img = image_handler.get_resized_image(removed_bg_img, 0.8, 0.8)

    imgUploader = S3ImageUploader()
    saved_image_url = imgUploader.upload_pil(resized_img, file_path)
    return saved_image_url
