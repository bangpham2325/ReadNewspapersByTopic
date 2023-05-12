import uuid

from django.db import models
from api_post.models import Posts


class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keyword = models.CharField(max_length=255, blank=True)
    post = models.ForeignKey(
        Posts, related_name="keywords", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "keyword"
