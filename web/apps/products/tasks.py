from celery import shared_task

@shared_task
def upload_image_by_url(img_url):
    return x + y