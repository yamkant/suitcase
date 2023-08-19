from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler

from users.constants import UserLevelEnum

from products.models import Product
from products.constants import CategoryEnum

class ProductViewSetListTest(ViewSetTestCase):
    endpoint = reverse_lazy('products:viewset')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_tester_user = TestUserHandler(
            email="tester@example.com",
            username="tester",
            phone="01050175933",
            password="5933"
        )
        general_user = cls.request_tester_user.get_user()
        general_user.level = UserLevelEnum.TESTER.value
        general_user.save()

        cls.data = {
            "name": "new_product",
            "image_url": "https://us.lemaire.fr/cdn/shop/files/PA326_LD1001_BR495_PS1_2000x.jpeg?v=1690202108",
            "saved_image_url": "https://s3_bucket_address/test_image.png",
            "category": CategoryEnum.PANTS.value,
            "user_id": general_user.id
        }
    
    def test_success(self):
        client = self.request_tester_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=201,
            client=client,
            name=self.data['name'],
            image_url=self.data['image_url'],
            saved_image_url=self.data['saved_image_url'],
            category=self.data['category'],
            user_id=self.data['user_id'],
        )

        test_field_list = ['name', 'image_url', 'saved_image_url', 'category', 'user_id']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], self.data[field])
    
    def test_failure_empty_name(self):
        client = self.request_tester_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            image_url=self.data['image_url'],
            saved_image_url=self.data['saved_image_url'],
            user_id=self.data['user_id'],
        )

    def test_failure_empty_image_url(self):
        client = self.request_tester_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            name=self.data['name'],
            user_id=self.data['user_id'],
        )

    def test_failure_empty_user_id(self):
        client = self.request_tester_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="post",
            expected_status_code=400,
            client=client,
            name=self.data['name'],
            image_url=self.data['image_url'],
        )