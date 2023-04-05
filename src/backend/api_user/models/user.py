import uuid
from django.utils.text import slugify
import pathlib
from django.db import models
from api_user.constants import Roles
from api_user.models import Account
from api_base.models import TimeStampedModel


def upload_path(instance, filename):
    fpath = pathlib.Path(filename)
    new_name = instance.avatar.name + str(uuid.uuid1())
    final_path = "/".join(
        ['avatars', slugify(f"{instance.full_name} {instance.id}")])

    return f"{final_path}/{new_name}{fpath.suffix}"


class User(TimeStampedModel):
    full_name = models.CharField(max_length=50)
    avatar = models.FileField(blank=True, null=True, upload_to=upload_path)
    role = models.CharField(choices=Roles.choices(), default=Roles.USER.value, max_length=50)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="user")

    class Meta:
            db_table = "users"
            ordering = ('-created_at',)
