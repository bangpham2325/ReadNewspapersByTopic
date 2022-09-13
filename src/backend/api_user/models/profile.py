from django.db import models
from api_user.constants import Roles
from api_user.models import Account
from api_base.models import TimeStampedModel


class Profile(TimeStampedModel):
    full_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(choices=Roles.choices(), default=Roles.USER.value, max_length=50)
    bio = models.TextField(null=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile")

    class Meta:
        db_table = "profiles"
        ordering = ('-created_at',)
