from django.db.models import (
    CharField,
    DateTimeField,
    BooleanField,
    IntegerField
)
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
    username: CharField         = CharField(max_length=30, unique=True)
    created_at: DateTimeField   = DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login: DateTimeField   = DateTimeField(verbose_name='last login', auto_now=True)
    is_admin: BooleanField      = BooleanField(default=False)
    is_active: BooleanField     = BooleanField(default=True)
    is_staff: BooleanField      = BooleanField(default=False)
    is_superuser:BooleanField   = BooleanField(default=False)
    level: IntegerField         = IntegerField(unique=False, default=1)
    user_url: CharField         = CharField(max_length=255, default="")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = 'users'