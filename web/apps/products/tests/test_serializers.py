from core.tests import IntegrationSerializerTestCase
from products.serializers import (
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)
from rest_framework.exceptions import ValidationError
from users.models import User
from products.models import Product
from products.constants import CategoryEnum
from django.shortcuts import get_object_or_404, get_list_or_404

from unittest import skip

EXCEPTION_MESSAGE = "이 필드는 필수 항목입니다."

@skip
class ProductCreateSerializerTestCase(IntegrationSerializerTestCase):
    serializer = ProductCreateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )
        cls.data = {
            "name": "new_product",
            "image_url": "https://s3_bucket_address/test_image.png",
            "category": CategoryEnum.PANTS.value,
        }

    def test_success(self):
        self.client.force_login(user=self.test_user)

        serializer = self.serializer_test(
            expected_query_count=2,
            instance=None,
            name=self.data['name'],
            image_url=self.data['image_url'],
            category=self.data['category'],
        )
        test_field_list = ['name', 'image_url', 'user_id', 'category']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], self.data[field])
    
    @skip
    def test_failure_empty_name(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                image_url=self.data['image_url'],
            )

    @skip
    def test_failure_empty_image_url(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                name=self.data['name'],
            )

    @skip
    def test_failure_empty_user_id(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                name=self.data['name'],
                image_url=self.data['image_url'],
            )


@skip
class ProductUpdateSerializerTestCase(IntegrationSerializerTestCase):
    serializer = ProductUpdateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        self.client.force_login(user=self.test_user)

        cls.test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )
        cls.data = {
            "name": "new_prod",
            "image_url": "https://s3_bucket_address/test_image.png",
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
            expected_query_count=1,
            instance=prod,
            name=self.update_data['name'],
            category=self.update_data['category'],
            is_active=self.update_data['is_active'],
        )

        test_field_list = ['name', 'category', 'is_active']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], self.update_data[field])
    
@skip
class ProductDeleteSerializerTestCase(IntegrationSerializerTestCase):
    serializer = ProductDeleteSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )
        cls.client.force_login(user=cls.test_user)
        cls.data = {
            "name": "new_prod",
            "image_url": "https://s3_bucket_address/test_image.png",
            "category": CategoryEnum.PANTS.value,
        }
        serializer = ProductCreateSerializer(data=cls.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cls.prod_data = serializer.data

        cls.update_data = {
            "is_deleted": "Y",
        }

    def test_success(self):
        prod = get_object_or_404(Product, id=self.prod_data['id'])

        serializer = self.serializer_test(
            expected_query_count=1,
            instance=prod,
            is_deleted=self.update_data['is_deleted'],
        )

        test_field_list = ['is_deleted']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], self.update_data[field])
    