from django.db import models

from api_base.models import TimeStampedModel
from api_post.models import Posts
from api_user.models import User
from api_interaction.constants import StarRating


class Rating(TimeStampedModel):
    title = models.CharField(max_length=50, default='Send Rating For Course')
    content = models.CharField(max_length=255, null=True, blank=True)
    star_rating = models.IntegerField(choices=StarRating.choices(), default=StarRating.FIVE.value)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    post = models.OneToOneField(Posts, null=True, blank=True, on_delete=models.SET_NULL, related_name="post_rating")

    class Meta:
        db_table = "rating"
        ordering = ('-created_at',)
