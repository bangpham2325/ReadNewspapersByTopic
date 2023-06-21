from django.db import models

from api_base.models import TimeStampedModel
from api_post.models import Posts
from api_user.models import User
from django.utils import timezone


class Bookmark(TimeStampedModel):
    bookmark_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookmark")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_bookmark")

    class Meta:
        db_table = "bookmark"
        ordering = ('-created_at',)
