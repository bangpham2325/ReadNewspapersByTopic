import uuid
from django.utils.text import slugify
import pathlib
from django.db import models
from api_user.constants import Roles
from api_user.models import Account
from api_base.models import TimeStampedModel


class User(TimeStampedModel):
    full_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(choices=Roles.choices(), default=Roles.USER.value, max_length=50)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(blank=True, null=True, related_name='user', to='api_post.Category')
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="user")
    bio = models.TextField(null=True)

    class Meta:
        db_table = "users"
        ordering = ('-created_at',)
