from django.urls import reverse_lazy
from django.test import TestCase
from core.libs.help_test import TestUserHandler
from users.constants import UserLevelEnum
from rest_framework import status
from unittest import skip

from users.models import User

class UserViewSetListTest(TestCase):
    endpoint = reverse_lazy('users:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.관리자_1 = User.objects.create(username="tester1", password="5933", level=UserLevelEnum.ADMIN.value)
        cls.일반_1 = User.objects.create(username="tester2", password="5933", level=UserLevelEnum.TESTER.value)

    def test_유저를_조회합니다(self):
        '''
        - 요청하는 유저의 정보만 입력되었기 때문에, 이에 대한 부분만 조회합니다.
        - admin 권한이 있는 user의 요청에 대해서만 응답합니다.
        '''
        self.client.force_login(user=self.관리자_1)

        response = self.client.get(path=self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

class UserViewSetDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.관리자_1 = User.objects.create(username="tester1", password="5933", level=UserLevelEnum.ADMIN.value)
        cls.일반_1 = User.objects.create(username="tester2", password="5933", level=UserLevelEnum.TESTER.value)

    def test_관리자유저는_다른_유저의_레벨을_수정한다(self):
        self.client.force_login(user=self.관리자_1)

        new_user = User.objects.create_user(
            username="new_user",
            password="5933"
        )

        fixture_data = {
            "level": UserLevelEnum.ADMIN.value,
        }

        endpoint = reverse_lazy('users:detail', args=[new_user.id])
        response = self.client.patch(path=endpoint, data=fixture_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_field_list = ['level']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(response.data[field], fixture_data[field])

    def test_일반유저는_다른_유저의_레벨을_수정할_수_없다(self):
        self.client.force_login(user=self.일반_1)

        new_user = User.objects.create_user(
            username="new_user",
            password="5933"
        )

        fixture_data = {
            "level": UserLevelEnum.ADMIN.value
        }

        endpoint = reverse_lazy('users:detail', args=[new_user.id])
        response = self.client.patch(path=endpoint, data=fixture_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_일반_유저는_자신의_url을_수정할_수_있다(self):
        self.client.force_login(user=self.일반_1)

        fixture_data = {
            "user_url": "test2@example.com",
        }

        endpoint = reverse_lazy('users:detail', args=[self.일반_1.id])
        response = self.client.patch(path=endpoint, data=fixture_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_field_list = ['user_url']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(response.data[field], fixture_data[field])