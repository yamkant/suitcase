from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler

from users.constants import UserLevelEnum

from products.models import Product

class ProductViewSetListTest(ViewSetTestCase):
    endpoint = reverse_lazy('products:viewset')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_general_user = TestUserHandler(
            email="general@example.com",
            username="general",
            phone="01050175933",
            password="5933"
        )
        general_user = cls.request_general_user.get_user()
        general_user.level = UserLevelEnum.GENERAL.value
        general_user.save()

        cls.data = {
            "name": "new_product",
            "image_url": "https://s3_bucket_address/test_image.png",
            "user_id": general_user.id
        }
    
    def test_success(self):
        client = self.request_general_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=201,
            client=client,
            name=self.data['name'],
            image_url=self.data['image_url'],
            user_id=self.data['user_id'],
        )

        test_field_list = ['name', 'image_url', 'user_id']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], self.data[field])
    
    def test_failure_empty_name(self):
        client = self.request_general_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            image_url=self.data['image_url'],
            user_id=self.data['user_id'],
        )

    def test_failure_empty_image_url(self):
        client = self.request_general_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            name=self.data['name'],
            user_id=self.data['user_id'],
        )

    def test_failure_empty_user_id(self):
        client = self.request_general_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            name=self.data['name'],
            image_url=self.data['image_url'],
        )