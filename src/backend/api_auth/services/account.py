from api_base.services import BaseService
from api_user.constants import Roles
from api_user.models import Account, User


class AccountService(BaseService):
    @classmethod
    def login_with_google(cls, account_obj, profile_obj):
        created_account = Account.objects.filter(email=account_obj['email'])
        if not created_account:
            account = Account.objects.create(**account_obj)
            profile_obj.update({
                'account_id': account.id,
                'role': Roles.USER.value,
            })
            return User.objects.create(**profile_obj)
        else:
            created_account.update(google_login=True)
        return User.objects.get_or_create(**profile_obj)[0]

    @classmethod
    def create_user(cls, validated_data):
        account = dict({
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        })
        account = Account.objects.filter(email=account['email']).update(**account)
        validated_data.update({'account': account})
        return User.objects.get_or_create(**validated_data)[0]
