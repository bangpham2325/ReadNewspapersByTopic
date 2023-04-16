from django.db import models
from api_base.models import TimeStampedModel


class Category(TimeStampedModel):
    title = models.CharField(default='', max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "category"
        ordering = ('-created_at',)
