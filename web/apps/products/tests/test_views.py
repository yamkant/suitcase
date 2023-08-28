from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler

from users.constants import UserLevelEnum

from products.models import Product
from products.constants import CategoryEnum
from products.serializers import ProductCreateSerializer

class ProductViewSetListTest(ViewSetTestCase):
    endpoint = reverse_lazy('products:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_tester_user = TestUserHandler(
            username="tester",
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

class ProductViewSetDetailTest(ViewSetTestCase):
    endpoint = reverse_lazy('products:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_tester_user = TestUserHandler(
            username="tester",
            password="5933"
        )
        general_user = cls.request_tester_user.get_user()
        general_user.level = UserLevelEnum.TESTER.value
        general_user.save()
        print("GENERAL USER================")
        print(general_user)

        cls.request_other_user = TestUserHandler(
            username="tester2",
            password="5933"
        )
        other_user = cls.request_other_user.get_user()
        other_user.level = UserLevelEnum.TESTER.value
        other_user.save()
        print("OTHER USER================")
        print(other_user)

        cls.data = {
            "name": "new_prod",
            "image_url": "https://s3_bucket_address/test_image.png",
            "user_id": general_user.id,
            "category": CategoryEnum.PANTS.value,
        }
        serializer = ProductCreateSerializer(data=cls.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cls.prod_data = serializer.data

        cls.other_data = {
            "name": "new_other_prod",
            "image_url": "https://s3_bucket_address/test_image.png",
            "user_id": other_user.id,
        }
        serializer = ProductCreateSerializer(data=cls.other_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cls.other_prod_data = serializer.data

        cls.update_data = {
            "name": "updated_product",
            "category": CategoryEnum.TOPS.value,
            "is_active": "N",
            "is_deleted": "Y",
        }
    
    def test_success_update(self):
        client = self.request_tester_user.get_loggedin_user()

        endpoint = reverse_lazy('products:detail', args=[self.prod_data['id']])

        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=200,
            client=client,
            name=self.update_data['name'],
            category=self.update_data['category'],
            is_active=self.update_data['is_active'],
        )

        test_field_list = ['name', 'category', 'is_active']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], self.update_data[field])

    def test_success_update_partial(self):
        client = self.request_tester_user.get_loggedin_user()
        print(self.request_tester_user.get_user())

        endpoint = reverse_lazy('products:detail', args=[self.prod_data['id']])

        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=200,
            client=client,
            is_active=self.update_data['is_active'],
        )

        test_field_list = ['is_active']

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], self.update_data[field])

    def test_failure_update__is_not_owner_user(self):
        client = self.request_tester_user.get_loggedin_user()

        endpoint = reverse_lazy('products:detail', args=[self.other_prod_data['id']])

        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=403,
            client=client,
            name=self.update_data['name'],
            category=self.update_data['category'],
            is_active=self.update_data['is_active'],
        )

    def test_success_delete(self):
        client = self.request_tester_user.get_loggedin_user()

        endpoint = reverse_lazy('products:detail', args=[self.prod_data['id']])

        res = self.generic_test(
            url=endpoint,
            method="delete",
            expected_status_code=200,
            client=client,
            is_deleted=self.update_data['is_deleted'],
        )

        test_field_list = ['is_deleted',]

        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], self.update_data[field])