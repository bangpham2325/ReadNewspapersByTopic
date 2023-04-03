import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from api_base.manager import UserManager


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    google_login = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = None
    last_name = None
    username = None
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "accounts"
        ordering = ('date_joined',)

    def __str__(self):
        return str(self.email)
