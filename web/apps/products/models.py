from django.db import models
from core.models import BaseModel
from users.models import User

class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=False)
    image_url = models.CharField(max_length=255)
    saved_image_url = models.CharField(max_length=255, blank=True, null=True)
    is_favorite = models.CharField(default="N", max_length=1)
    is_profile = models.CharField(default="N", max_length=1)
    category = models.IntegerField(default=1)
    is_active = models.CharField(default="Y", max_length=1)
    is_deleted = models.CharField(default="N", max_length=1)
    alarm_status = models.CharField(default="N", max_length=1)

    user_id = models.ForeignKey(User, db_column="user_id", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'products'