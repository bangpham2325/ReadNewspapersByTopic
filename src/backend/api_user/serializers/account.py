from rest_framework import serializers
from api_user.models import Account


class AccountSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Account
        fields = ['id', 'email', 'date_joined']
