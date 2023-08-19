from core.tests import IntegrationSerializerTestCase
from products.serializers import (
    ProductCreateSerializer,
)
from rest_framework.exceptions import ValidationError
from users.models import User
from products.constants import CategoryEnum

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


