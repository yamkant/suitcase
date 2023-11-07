from django.urls import reverse_lazy

from users.models import User
from products.models import Product
from users.constants import UserLevelEnum
from products.constants import CategoryEnum

from django.test import TestCase

from unittest import skip
from rest_framework import status

class ProductProfileViewSetTest(TestCase):
    endpoint = reverse_lazy('products:profile_list')

    user_1: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username="tester1", password="5933", level=UserLevelEnum.TESTER.value)
    
    # NOTE: 사품 조회 관련
    def test_로그인_이후_특정_카테고리를_좋아요_한다(self):
        self.client.force_login(user=self.user_1)

        self.prod_1 = Product.objects.create(
            name="new_prod_1",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=self.user_1,
        )
        
        request_data = {
            'prod_id': self.prod_1.id,
            'category': CategoryEnum.TOPS.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')
        self.prod_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], request_data['category'])
    
    def test_하나의_카테고리에_대해서_하나의_프로필만_설정한다(self):
        self.client.force_login(user=self.user_1)

        self.prod_1 = Product.objects.create(
            name="new_prod_1",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=self.user_1,
        )
        
        request_data = {
            'prod_id': self.prod_1.id,
            'category': CategoryEnum.TOPS.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')
        self.prod_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], request_data['category'])