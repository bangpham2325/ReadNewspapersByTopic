from rest_framework import serializers
from api_auth.services import AccountService, Google, register_social_user
from api_user.constants import Roles
from api_user.models import Account, User
from rest_framework.exceptions import AuthenticationFailed
import os


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'avatar', 'address', 'role', 'phone', 'birthday', 'password']
        extra_kwargs = {
            'avatar': {'required': False},
            'phone': {'required': False},
            'role': {'required': False},
            'birthday': {'required': False},
        }

    def to_internal_value(self, data):
        context = self.context.get('view')
        if context and context.action in ['admin'] and context.action in ['create']:
            data['password'] = '1345'
        return super().to_internal_value(data)

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['admin']:
            kwargs = dict({'required': False})
            extra_kwargs['password'] = kwargs
        return extra_kwargs

    def create(self, validated_data):
        account = dict({
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        })
        account = Account.objects.create_user(**account)
        validated_data.update({
            'account': account,
        })
        return User.objects.create(**validated_data)


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(provider=provider, user_id=user_id, email=email, name=name)

    def to_representation(self, instance):
        data = instance
        user_id = Account.objects.get(email=data['email']).user.id
        data = {"user_id": user_id,
                "username": data['username'],
                "email": data['email'],
                "access_token": str(data['tokens'].access_token),
                "refresh_token": str(data['tokens']),
                }
        return data
