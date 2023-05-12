import uuid

from django.db import models
from api_base.models import TimeStampedModel
from api_post.models import Posts


class Contents(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=255, blank=True)
    paragraph = models.JSONField(blank=True)
    description_img = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    post = models.ForeignKey(
        Posts, related_name="contents", on_delete=models.CASCADE, null=True, blank=True
    )
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "contents"
        ordering = ["-created_at"]
