from django.core.management.base import BaseCommand

from core.classes import S3ImageUploader, ImageHandler

# TODO: log 추가
import logging

logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    help = '서비스를 위해 필요한 권한을 생성합니다.'

    def handle(self, *args, **kwargs):
        img_url = "https://us.lemaire.fr/cdn/shop/files/PA326_LD1001_BR495_PS1_2000x.jpeg?v=1690202108"

        image_handler = ImageHandler(img_url)
        removed_bg_img = image_handler.get_removed_background_image()

        imgUploader = S3ImageUploader()
        filename = S3ImageUploader.get_file_name('test')
        imgUploader.upload_pil(removed_bg_img, filename)
