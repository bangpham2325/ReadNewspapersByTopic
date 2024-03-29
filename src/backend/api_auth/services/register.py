
from django.contrib.auth import authenticate
from api_user.models import User, Account
import os
from api_user.services import UserService
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = Account.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            account = filtered_user_by_email.first()
            token = RefreshToken.for_user(account)

            return {
                'username': account.username,
                'email': account.email,
                'tokens': token
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        account = dict({
            'email': email,
            'password': os.environ.get('SOCIAL_SECRET')})
        account = Account.objects.create_user(**account)
        account.username = name
        account.is_verified = True
        account.auth_provider = provider
        account.save()
        user = dict({
            'account': account,
            'full_name': name
        })
        User.objects.create(**user)
        token = RefreshToken.for_user(account)
        return {
            'email': email,
            'username': str(name),
            'tokens': token
        }
