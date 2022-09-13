from rest_framework import serializers
from api_user.models import User
from api_user.serializers import AccountSerializer


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'role', 'avatar', 'bio', 'address',
                  'phone', 'birthday', 'account']

        extra_kwargs = {
            'full_name': {'required': False},
            'avatar': {'required': False},
            'phone': {'required': False},
            'birthday': {'required': False},
        }


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'role', 'avatar']
