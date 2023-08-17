from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성, username 이 userID를 의미함
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have an userID.")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 User 생성
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email        = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username     = models.CharField(max_length=30, unique=True)
    phone        = models.CharField(max_length=11, null=False, blank=False)
    created_at   = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    level        = models.IntegerField(unique=False, default=1)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    class Meta:
        db_table = 'users'