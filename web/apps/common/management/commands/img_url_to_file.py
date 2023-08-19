from django.core.management.base import BaseCommand
from PIL import Image
import requests
from io import BytesIO
from rembg import remove

from core.classes import S3ImageUploader

# TODO: log 추가
import logging

logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class Command(BaseCommand):
    help = '서비스를 위해 필요한 권한을 생성합니다.'

    def handle(self, *args, **kwargs):
        img_url = "https://us.lemaire.fr/cdn/shop/files/PA326_LD1001_BR495_PS1_2000x.jpeg?v=1690202108"
        response = requests.get(img_url)
        img_data = BytesIO(response.content)

        image = Image.open(img_data)

        rembg_image = remove(image)
        new_width = int(rembg_image._size[0] * 0.8)
        new_height = int(rembg_image._size[1] * 0.8)
        resized_img = image.resize((new_width, new_height))

        imgUploader = S3ImageUploader()
        imgUploader.upload_pil(resized_img, 'test/test_img2.png')
