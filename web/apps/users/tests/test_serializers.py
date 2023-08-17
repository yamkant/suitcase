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
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
            password2="5933"
        )

        fixture_data = {
            "email": "test@example.com",
            "username": "yamkim",
            "phone": "01050175933",
        }
        self.assertEqual(serializer.data, fixture_data)

        # NOTE: skill
        # for field, expected in fixture_data:
        #     with self.subTest(field=field, expected=expected):
        #         # self.assertEqual(getattr(serializer, field), expected)
        #         self.assertEqual(serializer, expected)

    def test_failure_without_email(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                username="yamkim",
                phone="01050175933",
                password="5933",
                password2="5933"
            )

    def test_failure_without_username(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                email="test@example.com",
                phone="01050175933",
                password="5933",
                password2="5933"
            )

    def test_failure_without_password(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                email="test@example.com",
                phone="01050175933",
                username="yamkim",
                password2="5933"
            )

    def test_failure_without_password2(self):
        with self.assertRaisesMessage(ValidationError, EXCEPTION_MESSAGE):
            serializer = self.serializer_test(
                email="test@example.com",
                phone="01050175933",
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
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
        )
        serializer = self.serializer_test(test_user)
        fixture_data = {
            "id": test_user.id,
            "email": "test@example.com",
            "username": "yamkim",
            "phone": "01050175933",
            "level": UserLevelEnum.GENERAL.value
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
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
        )
        data = {
            "username": "yamkant",
            "level": UserLevelEnum.ADMIN.value,
        }

        fixture_data = {
            "id": test_user.id,
            "email": test_user.email,
            "username": data['username'],
            "phone": test_user.phone,
            "level": test_user.level,
        }
        serializer = self.serializer_test(test_user, **data)
        self.assertEqual(serializer.data, fixture_data)

class UserUpdateForAdminLevelSerializerTestCase(IntegrationSerializerTestCase):
    serializer = UserUpdateForAdminLevelSerializer
    
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_success(self):
        test_user = User.objects.create_user(
            email="test@example.com",
            username="yamkim",
            phone="01050175933",
            password="5933",
        )
        data = {
            "username": "yamkant",
            "level": UserLevelEnum.ADMIN.value,
        }
        fixture_data = {
            "id": test_user.id,
            "email": test_user.email,
            "username": data['username'],
            "phone": test_user.phone,
            "level": data['level'],
        }
        serializer = self.serializer_test(test_user, **data)
        self.assertEqual(serializer.data, fixture_data)