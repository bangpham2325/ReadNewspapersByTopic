import uuid
import pathlib
from django.db import models
from api_base.models import TimeStampedModel
from api_post.models import Category, Source
from django.utils.text import slugify
from api_post.constants import PostStatus
from django.utils import timezone
from api_user.models import User


def upload_path(instance, filename):
    fpath = pathlib.Path(filename)
    new_name = str(uuid.uuid1())
    final_path = "/".join(
        ['posts', slugify(f"{instance.title} {instance.author}"), 'thumbnail'])

    return f"{final_path}/{new_name}{fpath.suffix}"


class Posts(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, null=True)
    content = models.TextField()
    thumbnail = models.FileField(blank=True, null=True, upload_to=upload_path)
    category = models.ManyToManyField(
        Category, related_name="posts", null=True, blank=True
    )
    source = models.OneToOneField(
        Source, related_name="posts", on_delete=models.SET_NULL, null=True, blank=True
    )
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_by", null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    status = models.CharField(choices=PostStatus.choices(), default=PostStatus.DRAFT.value, max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]