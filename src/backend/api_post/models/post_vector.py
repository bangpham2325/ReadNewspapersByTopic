import uuid
import pathlib
from django.db import models
from api_base.models import TimeStampedModel
from api_post.models import Posts


class PostVector(TimeStampedModel):
    post = models.OneToOneField(Posts, on_delete=models.CASCADE)
    vector = models.BinaryField()

    class Meta:
        db_table = "post_vector"
        ordering = ["-created_at"]
