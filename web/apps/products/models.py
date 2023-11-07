from django.db.models import (
    Model,
    Manager, 
    AutoField,
    CharField,
    IntegerField,
    ForeignKey,
    CASCADE,
)
from apps.core.models import BaseModel
from apps.users.models import User

class ActiveProductManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted="N")

    def get_in_list(self, prod_id_list):
        return self.get_queryset().filter(id__in=prod_id_list)

class Product(BaseModel):
    id: AutoField               = AutoField(primary_key=True)
    name: CharField             = CharField(max_length=255, unique=False)
    image_url: CharField        = CharField(max_length=255)
    saved_image_url: CharField  = CharField(max_length=255, blank=True, null=True)
    is_profile: CharField       = CharField(default="N", max_length=1)
    category: IntegerField      = IntegerField(default=1)
    is_active: CharField        = CharField(default="Y", max_length=1)
    is_deleted: CharField       = CharField(default="N", max_length=1)

    user_id: ForeignKey         = ForeignKey(User, db_column="user_id", on_delete=CASCADE)

    objects: Manager            = Manager()
    active_objects:ActiveProductManager = ActiveProductManager()

    class Meta:
        managed = True
        db_table = 'products'

class ProductProfile(Model):
    id: AutoField               = AutoField(primary_key=True)
    prod_id: ForeignKey         = ForeignKey(Product, db_column="prod_id", on_delete=CASCADE)
    category: IntegerField      = IntegerField(default=1, unique=True)

    class Meta:
        managed = True
        db_table = 'product_profiles'