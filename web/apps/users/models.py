from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성, username 이 userID를 의미함
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an userID.")
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username     = models.CharField(max_length=30, unique=True)
    created_at   = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    level        = models.IntegerField(unique=False, default=1)
    user_url     = models.CharField(max_length=255, default="")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = 'users'