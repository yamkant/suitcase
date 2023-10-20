from django.db import models
from core.models import BaseModel
from users.models import User

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted="N")

    def get_in_list(self, prod_id_list):
        return self.get_queryset().filter(id__in=prod_id_list)

class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=False)
    image_url = models.CharField(max_length=255)
    saved_image_url = models.CharField(max_length=255, blank=True, null=True)
    is_profile = models.CharField(default="N", max_length=1)
    category = models.IntegerField(default=1)
    is_active = models.CharField(default="Y", max_length=1)
    is_deleted = models.CharField(default="N", max_length=1)

    user_id = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)

    objects = models.Manager()
    active_objects = ActiveProductManager()

    class Meta:
        managed = True
        db_table = 'products'

class ProductProfile(models.Model):
    id = models.AutoField(primary_key=True)
    prod_id = models.ForeignKey(Product, db_column="prod_id", on_delete=models.CASCADE)
    category = models.IntegerField(default=1, unique=True)

    class Meta:
        managed = True
        db_table = 'product_profiles'