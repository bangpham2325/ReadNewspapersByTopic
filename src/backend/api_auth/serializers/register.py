from rest_framework import serializers

from api_auth.services import AccountService
from api_user.constants import Roles
from api_user.models import Account, User


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
        if context and context.action in ['admin'] or context and context.action in ['create']:
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
