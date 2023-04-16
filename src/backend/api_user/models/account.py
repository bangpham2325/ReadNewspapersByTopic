import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from api_base.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    google_login = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None
    first_name = None
    last_name = None
    EMAIL_FIELD = 'email'
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "accounts"
        ordering = ('date_joined',)

    def __str__(self):
        return str(self.email)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
