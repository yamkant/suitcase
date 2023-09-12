from django.core.management.base import BaseCommand

from core.classes import S3ImageUploader, ImageHandler
from products.tasks import upload_image_by_image_url

from products.tasks import (
    upload_image_by_image_url,
)

# TODO: log 추가
import logging

logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    help = '서비스를 위해 필요한 권한을 생성합니다.'

    def handle(self, *args, **kwargs):
        # img_url = "https://us.lemaire.fr/cdn/shop/files/PA326_LD1001_BR495_PS1_2000x.jpeg?v=1690202108"
        img_url = "https://noclaim.co.kr/web/product/extra/small/202211/d0e03850b5704618babeef3269d22cd1.jpg"

        upload_image_by_image_url.delay(img_url, 'tester')