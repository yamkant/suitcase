from django.urls import reverse_lazy

from users.models import User
from products.models import Product
from users.constants import UserLevelEnum
from products.constants import CategoryEnum
from products.constants import ProductStatusEnum, ProductDeleteEnum

from django.test import TestCase

from unittest import skip
from rest_framework import status

class ProductViewSetListTest(TestCase):
    endpoint = reverse_lazy('products:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username="tester1", password="5933", level=UserLevelEnum.TESTER.value)
    
    # NOTE: 사품 조회 관련
    def test_로그인_이후_상품을_조회한다(self):
        self.client.force_login(user=self.user_1)

        self.prod_1 = Product.objects.create(
            name="new_prod_1",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=self.user_1,
        )

        self.prod_2 = Product.objects.create(
            name="new_prod_2",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=self.user_1,
        )
        
        response = self.client.get(path=self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        list_data = response.json()['results']
        self.assertEqual(
            list_data,
            sorted(list_data, key=lambda x: x['id'], reverse=True)
        )

    def test_페이지_정보와_함께_상품을_조회한다(self):
        self.client.force_login(user=self.user_1)

        endpoint = self.endpoint + '?page=2&page_size=1'

        self.prod_1 = Product.objects.create(name="new_prod_1", user_id=self.user_1)
        self.prod_2 = Product.objects.create(name="new_prod_2", user_id=self.user_1)
        self.prod_3 = Product.objects.create(name="new_prod_2", user_id=self.user_1)
        
        response = self.client.get(path=endpoint, content_type='application/json')
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data['count'], 3)
        self.assertEqual(res_data['results'][0]['id'], self.prod_2.id)

    def test_로그인_이후_상품을_생성한다(self):
        self.client.force_login(user=self.user_1)

        request_data = {
            'name': '상품_1',
            'image_url': 'http://example.com',
            'category': CategoryEnum.UNDEFINED.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_field_list = ['name', 'image_url', 'category']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(response.data[field], request_data[field])

    # NOTE: 상품 생성 관련
    def test_로그인하지_않으면_상품을_생성할_수_없다(self):
        request_data = {
            'name': '상품_1',
            'image_url': 'http://example.com',
            'category': CategoryEnum.UNDEFINED.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_상품이름을_입력하지_않으면_생성되지_않는다(self):
        self.client.force_login(user=self.user_1)

        request_data = {
            'image_url': 'http://example.com',
            'category': CategoryEnum.UNDEFINED.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_상품의_이미지를_입력하지_않으면_생성되지_않는다(self):
        self.client.force_login(user=self.user_1)

        request_data = {
            'name': '상품_1',
            'category': CategoryEnum.UNDEFINED.value,
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_상품의_카테고리를_입력하지_않으면_UNDIFINED로_설정된다(self):
        self.client.force_login(user=self.user_1)

        request_data = {
            'name': '상품_1',
            'image_url': 'http://example.com',
        }

        response = self.client.post(path=self.endpoint, data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_field_list = ['name', 'image_url', 'category']
        request_data['category'] = CategoryEnum.UNDEFINED.value
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(response.data[field], request_data[field])

class ProductViewSetDetailTest(TestCase):
    endpoint = reverse_lazy('products:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create_user(username="tester1", password="5933")
        cls.user_2 = User.objects.create_user(username="tester2", password="5933")

        cls.prod = Product.objects.create(
            name="new_prod",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=cls.user_1,
        )

        cls.other_prod = Product.objects.create(
            name="new_other_prod",
            image_url="https://s3_bucket_address/test_image.png",
            category=CategoryEnum.PANTS.value,
            user_id=cls.user_2,
        )
    
    # NOTE: 상품 개별 수정 관련
    def test_상품의_이름을_수정한다(self):
        self.client.force_login(user=self.user_1)
        endpoint = reverse_lazy('products:detail', args=[self.prod.id])

        request_data = {
            "name": "수정된 이름",
        }

        response = self.client.patch(path=endpoint, data=request_data, content_type='application/json')
        self.prod.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], request_data['name'])


    def test_상품_활성화_상태를_수정한다(self):
        self.client.force_login(user=self.user_1)
        endpoint = reverse_lazy('products:detail', args=[self.prod.id])

        request_data = {
            "is_active": ProductStatusEnum.ACTIVE.value,
        }

        response = self.client.patch(path=endpoint, data=request_data, content_type='application/json')
        self.prod.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_active'], request_data['is_active'])
    
    def test_상품을_논리적_삭제한다(self):
        self.client.force_login(user=self.user_1)
        endpoint = reverse_lazy('products:detail', args=[self.prod.id])

        request_data = {
        }

        response = self.client.delete(path=endpoint, data=request_data, content_type='application/json')
        self.prod.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_deleted'], ProductDeleteEnum.DELETED.value)

    def test_타인의_상품을_수정할_수_없다(self):
        self.client.force_login(user=self.user_1)

        endpoint = reverse_lazy('products:detail', args=[self.other_prod.id])

        request_data = {
            'name': '수정된 이름'
        }

        response = self.client.patch(path=endpoint, data=request_data, content_type='application/json')
        self.prod.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # NOTE: 상품 개별 삭제 관련
    def test_타인의_상품을_삭제할_수_없다(self):
        self.client.force_login(user=self.user_1)

        endpoint = reverse_lazy('products:detail', args=[self.other_prod.id])

        request_data = {
        }

        response = self.client.delete(path=endpoint, data=request_data, content_type='application/json')
        self.prod.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)