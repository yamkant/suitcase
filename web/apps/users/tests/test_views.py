from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler
from users.constants import UserLevelEnum

from users.models import User

class UserViewSetListTest(ViewSetTestCase):
    endpoint = reverse_lazy('users:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_admin_user = TestUserHandler(
            username="admin",
            password="5933"
        )
        admin_user = cls.request_admin_user.get_user()
        admin_user.level = UserLevelEnum.ADMIN.value
        admin_user.save()

        cls.request_general_user = TestUserHandler(
            username="general",
            password="5933"
        )
        general_user = cls.request_general_user.get_user()
        general_user.level = UserLevelEnum.GENERAL.value
        general_user.save()

    def test_success(self):
        '''
        - 요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.
        - admin 권한이 있는 user의 요청에 대해서만 응답합니다.
        '''
        client = self.request_admin_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="get",
            expected_status_code=200,
            client=client,
        )

        self.assertEqual(len(res.json()), 2)

    def test_success_unauthorized_user(self):
        '''
        - 요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.
        - admin 권한이 없기 때문에 권한 제한 status code를 반환합니다.
        '''
        unauthorized_test_request_user = TestUserHandler(
            username="unauthorized_tester",
            password="5933"
        )
        client = unauthorized_test_request_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="get",
            expected_status_code=200,
            client=client,
        )
        self.assertEqual(len(res.json()), 3)


class UserViewSetDetailTest(ViewSetTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.request_admin_user = TestUserHandler(
            username="tester",
            password="5933"
        )
        admin_user = cls.request_admin_user.get_user()
        admin_user.level = UserLevelEnum.ADMIN.value
        admin_user.save()

        cls.request_general_user = TestUserHandler(
            username="general",
            password="5933"
        )
        general_user = cls.request_general_user.get_user()
        general_user.level = UserLevelEnum.GENERAL.value
        general_user.save()

    def test_success(self):
        '''
        - admin user는 다른 user의 level까지 수정 가능합니다.
        '''
        client = self.request_admin_user.get_loggedin_user()

        new_user = User.objects.create_user(
            username="new_user",
            password="5933"
        )

        fixture_data = {
            "level": UserLevelEnum.ADMIN.value
        }

        endpoint = reverse_lazy('users:detail', args=[new_user.id])
        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=200,
            client=client,
            level=fixture_data['level'],
        )

        test_field_list = ['level']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], fixture_data[field])

    def test_failure_update_level_with_general_user(self):
        '''
        - general user는 다른 user의 level을 수정하는 권한은 가지고 있지 않습니다.
        '''
        client = self.request_general_user.get_loggedin_user()

        new_user = User.objects.create_user(
            username="new_user",
            password="5933"
        )

        fixture_data = {
            "level": UserLevelEnum.ADMIN.value
        }

        endpoint = reverse_lazy('users:detail', args=[new_user.id])
        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=401,
            client=client,
            level=fixture_data['level'],
        )

    def test_success_update_user_url_with_general_user(self):
        '''
        - user의 level 외의 값은 수정 가능합니다.
        '''
        client = self.request_general_user.get_loggedin_user()

        new_user = User.objects.create_user(
            username="new_user",
            password="5933",
        )
        new_user.user_url = "test@example.com"
        new_user.save()

        fixture_data = {
            "user_url": "test2@example.com",
        }

        endpoint = reverse_lazy('users:detail', args=[new_user.id])
        res = self.generic_test(
            url=endpoint,
            method="patch",
            expected_status_code=200,
            client=client,
            user_url=fixture_data['user_url'],
        )

        test_field_list = ['user_url']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(res.json()[field], fixture_data[field])