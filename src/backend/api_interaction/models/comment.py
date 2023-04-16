from django.db import models

from api_base.models import TimeStampedModel
from api_post.models import Posts
from api_user.models import User


class Comment(TimeStampedModel):
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_comment")
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="child_comments")

    class Meta:
        db_table = "comments"
        ordering = ('-created_at',)
