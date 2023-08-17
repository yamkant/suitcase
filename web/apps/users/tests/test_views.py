from django.urls import reverse_lazy
from core.tests import ViewSetTestCase
from core.libs.help_test import TestUserHandler

from users.models import User

class UserPermissionViewSetTest(ViewSetTestCase):
    endpoint = reverse_lazy('users:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_request_user = TestUserHandler(
            email="test1@example.com",
            username="tester",
            phone="01050175933",
            password="5933"
        )

    def test_success(self):
        '''요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.'''
        client = self.test_request_user.get_loggedin_user()

        res = self.generic_test(
            url=self.endpoint,
            method="get",
            expected_status_code=200,
            client=client,
        )

        self.assertEqual(len(res.json()), 1)