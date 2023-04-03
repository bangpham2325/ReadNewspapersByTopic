from api_base.services import BaseService
from api_user.constants import Roles
from api_user.models import Account, User
from itertools import groupby


class UserService(BaseService):
    @classmethod
    def create_user(cls, validated_data):
        account = dict({
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        })
        if validated_data.get('role') is Roles.ADMIN.value:
            account = Account.objects.create_superuser(**account)
        elif validated_data.get('role') is Roles.ADMIN.value:
            account = Account.objects.create_staff(**account)
        else:
            account = Account.objects.create_user(**account)
        validated_data.update({'account': account})
        return User.objects.create(**validated_data)

    @classmethod
    def get_all_users(cls):
        profiles = User.objects.filter().order_by('role')
        res_data = []
        for role, profile in groupby(profiles, lambda x: x.role):
            res_data.append((role, [i for i in profile]))
        return res_data
