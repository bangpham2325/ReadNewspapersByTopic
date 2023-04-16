from django.db import models
from api_base.models import TimeStampedModel


class Source(TimeStampedModel):
    title = models.CharField(default='', max_length=255)
    domain = models.CharField(max_length=255, blank=True, unique=True)

    class Meta:
        db_table = "source"
        ordering = ('-created_at',)
