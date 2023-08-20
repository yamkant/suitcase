from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductCreateSerializer
)
from users.constants import UserLevelEnum

from PIL import Image
import requests
from io import BytesIO
from rembg import remove
from core.classes import S3ImageUploader

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    serializer_action_classes = {
        'list': ProductSerializer,
        'create': ProductCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class

    def create(self, request, *args, **kwargs):
        if request.user.level == UserLevelEnum.TESTER.value:
            return super().create(request, *args, **kwargs)

        # TODO: 리팩토링 예정
        request.POST._mutable = True
        
        response = requests.get(request.data['image_url'])
        img_data = BytesIO(response.content)
        image = Image.open(img_data)
        rembg_image = remove(image)
        new_width = int(rembg_image._size[0] * 0.8)
        new_height = int(rembg_image._size[1] * 0.8)
        resized_img = rembg_image.resize((new_width, new_height))

        imgUploader = S3ImageUploader()
        request.data['saved_image_url'] = imgUploader.upload_pil(resized_img, f'{request.user.username}')
        request.data['user_id'] = request.user.id

        return super().create(request, *args, **kwargs)
