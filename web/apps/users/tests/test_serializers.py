from core.tests import IntegrationSerializerTestCase
from users.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateForGeneralLevelSerializer,
    UserUpdateForAdminLevelSerializer
)

from users.models import User
from users.constants import UserLevelEnum
from unittest import skip
from rest_framework.exceptions import ValidationError

EXCEPTION_MESSAGE = "이 필드는 필수 항목입니다."

class UserCreateSerializerTestCase(IntegrationSerializerTestCase):
    serializer = UserCreateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_success(self):
        serializer = self.serializer_test(
            username="yamkim",
            password="5933",
            password2="5933"
        )

        fixture_data = {
            "username": "yamkim",
        }
        # self.assertEqual(serializer.data, fixture_data)

        # NOTE: skill
        for field, expected in fixture_data.items():
            with self.subTest(field=field, expected=expected):
                self.assertEqual(serializer.data[field], expected)

    def test_failure_without_username(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                password="5933",
                password2="5933"
            )

    def test_failure_without_password(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                username="yamkim",
                password2="5933"
            )

    def test_failure_without_password2(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                username="yamkim",
                password="5933"
            )

class UserSerializerTestCase(IntegrationSerializerTestCase):
    serializer = UserSerializer
    
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_success(self):
        test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )
        serializer = self.serializer_test(instance=test_user)
        fixture_data = {
            "id": test_user.id,
            "username": "yamkim",
            "level": UserLevelEnum.GENERAL.value,
            "user_url": "",
        }

        self.assertEqual(serializer.data, fixture_data)

class UserUpdateForGeneralLevelSerializerTestCase(IntegrationSerializerTestCase):
    serializer = UserUpdateForGeneralLevelSerializer
    
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_success(self):
        '''
        - level을 수정할 권한은 가지고 있지 않습니다.
        '''
        test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )

        fixture_data = {
            "level": test_user.level,
            "user_url": "test@example.com",
        }
        serializer = self.serializer_test(
            instance=test_user,
            user_url=fixture_data["user_url"],
        )

        test_field_list = ['level', 'user_url']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], fixture_data[field])

class UserUpdateForAdminLevelSerializerTestCase(IntegrationSerializerTestCase):
    serializer = UserUpdateForAdminLevelSerializer
    
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_success(self):
        test_user = User.objects.create_user(
            username="yamkim",
            password="5933",
        )
        data = {
            "level": UserLevelEnum.ADMIN.value,
        }
        fixture_data = {
            "level": data['level'],
        }
        serializer = self.serializer_test(instance=test_user, **data)

        test_field_list = ['level']
        for field in test_field_list:
            with self.subTest(field=field):
                self.assertEqual(serializer.data[field], fixture_data[field])