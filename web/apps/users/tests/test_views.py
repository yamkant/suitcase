from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler
from users.constants import UserLevelEnum

from users.models import User

class UserPermissionViewSetTest(ViewSetTestCase):
    endpoint = reverse_lazy('users:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_request_user = TestUserHandler(
            email="admin@example.com",
            username="tester",
            phone="01050175933",
            password="5933"
        )
        admin_user = cls.test_request_user.get_user()
        admin_user.level = UserLevelEnum.ADMIN.value
        admin_user.save()

    def test_success(self):
        '''
        - 요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.
        - admin 권한이 있는 user의 요청에 대해서만 응답합니다.
        '''
        client = self.test_request_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="get",
            expected_status_code=200,
            client=client,
        )

        self.assertEqual(len(res.json()), 1)

    def test_success_unauthorized_user(self):
        '''
        - 요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.
        - admin 권한이 없기 때문에 권한 제한 status code를 반환합니다.
        '''
        unauthorized_test_request_user = TestUserHandler(
            email="user@example.com",
            username="unauthorized_tester",
            phone="01050175933",
            password="5933"
        )
        client = unauthorized_test_request_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="get",
            expected_status_code=200,
            client=client,
        )
        self.assertEqual(len(res.json()), 2)
