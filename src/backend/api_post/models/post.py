import uuid
import pathlib
from django.db import models
from api_base.models import TimeStampedModel
from api_post.models import Category, Source
from django.utils.text import slugify
from api_post.constants import PostStatus
from django.utils import timezone
from api_user.models import User


class Posts(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name="posts", null=True, blank=True, on_delete=models.SET_NULL
    )
    source = models.OneToOneField(
        Source, related_name="posts", on_delete=models.CASCADE, null=True, blank=True
    )
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_by", null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    status = models.CharField(choices=PostStatus.choices(), default=PostStatus.DRAFT.value, max_length=50)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]
