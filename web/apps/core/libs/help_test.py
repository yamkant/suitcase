from users.models import User
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

class TestUserHandler():
    def __init__(self, **kwargs) -> None:
        self._client = APIClient()
        self._data = kwargs
        self._user = self.create_user(**kwargs)
    
    def create_user(self, **kwargs):
        test_user = User.objects.create_user(**kwargs)
        return test_user

    def get_user(self):
        return self._user
    
    def get_loggedin_user(self):
        is_logined = self._client.login(
            username=self._user.username,
            password=self._data['password'], # login시 hashing 처리
        )
        return self._client

    def get_not_loggedin_user(self):
        return APIClient()