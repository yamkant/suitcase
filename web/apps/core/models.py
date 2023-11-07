from django.db.models import (
    Model,
    DateTimeField,
)

class BaseModel(Model):
    updated_at: DateTimeField = DateTimeField(
        auto_now=True,
    )
    created_at: DateTimeField = DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
