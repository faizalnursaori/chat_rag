from django.db import models

from .utils import generate_id


class BaseModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=generate_id)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
