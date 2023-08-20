from core.tests import IntegrationSerializerTestCase
from products.serializers import (
    ProductCreateSerializer,
    ProductUpdateSerializer,
)
from rest_framework.exceptions import ValidationError
from users.models import User
from products.models import Product
from products.constants import CategoryEnum
from django.shortcuts import get_object_or_404, get_list_or_404

EXCEPTION_MESSAGE = "이 필드는 필수 항목입니다."

class ProductCreateSerializerTestCase(IntegrationSerializerTestCase):
    serializer = ProductCreateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create_user(
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
        )
        cls.data = {
            "name": "new_product",
            "image_url": "https://s3_bucket_address/test_image.png",
            "user_id": cls.test_user.id,
            "category": CategoryEnum.PANTS.value,
        }

    def test_success(self):
        serializer = self.serializer_test(
            name=self.data['name'],
            image_url=self.data['image_url'],
            user_id=self.data['user_id'],
            category=self.data['category'],
        )
        test_field_list = ['name', 'image_url', 'user_id', 'category']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], self.data[field])
    
    def test_failure_empty_name(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                image_url=self.data['image_url'],
                user_id=self.data['user_id'],
            )

    def test_failure_empty_image_url(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                name=self.data['name'],
                user_id=self.data['user_id'],
            )

    def test_failure_empty_user_id(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                name=self.data['name'],
                image_url=self.data['image_url'],
            )


class ProductUpdateSerializerTestCase(IntegrationSerializerTestCase):
    serializer = ProductUpdateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create_user(
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
        )
        cls.data = {
            "name": "new_prod",
            "image_url": "https://s3_bucket_address/test_image.png",
            "user_id": cls.test_user.id,
            "category": CategoryEnum.PANTS.value,
        }
        serializer = ProductCreateSerializer(data=cls.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cls.prod_data = serializer.data

        cls.update_data = {
            "name": "updated_product",
            "category": CategoryEnum.TOPS.value,
            "is_active": "N",
            "is_deleted": "Y",
        }

    def test_success(self):
        prod = get_object_or_404(Product, id=self.prod_data['id'])

        serializer = self.serializer_test(
            prod,
            name=self.update_data['name'],
            category=self.update_data['category'],
            is_active=self.update_data['is_active'],
            is_deleted=self.update_data['is_deleted'],
        )

        test_field_list = ['name', 'category', 'is_active', 'is_deleted']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], self.update_data[field])
    