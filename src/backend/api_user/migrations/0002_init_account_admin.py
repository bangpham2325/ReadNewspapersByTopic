from django.conf import settings
from django.db import migrations
from django.contrib.auth.hashers import make_password
from api_user.constants import Roles


def init_admin_account(apps, schema_editor):
    account = apps.get_model("api_user", "Account")
    user = apps.get_model("api_user", "User")

    account_obj = dict({
        'email': 'admin@gmail.com',
        'password': make_password(
            password='123456', salt=settings.SECRET_KEY
        ),
        'is_staff': True,
        'is_superuser': True
    })
    created_account = account.objects.create(**account_obj)
    user_obj = dict({
        'account_id': created_account.id,
        'full_name': 'admin',
        'role': Roles.ADMIN.value,
    })
    return user.objects.create(**user_obj)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_admin_account, migrations.RunPython.noop),
        migrations.AlterModelManagers(
            name='account',
            managers=[
            ],
        ),
    ]
