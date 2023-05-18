from rest_framework import serializers
from api_user.models import User
from api_user.serializers import AccountSerializer
from api_user.services import UserService

from api_post.models import Category
from rest_framework.fields import UUIDField


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True,
                                                      queryset=Category.objects.all(), pk_field=UUIDField(format='hex'),
                                                      source='categories')
    categories = CategoryShortSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'role', 'avatar', 'address',
                  'phone', 'birthday', 'account', 'category_ids', 'categories']

        extra_kwargs = {
            'full_name': {'required': False},
            'avatar': {'required': False},
            'phone': {'required': False},
            'birthday': {'required': False},
            'category_ids': {'required': False},
            'categories': {'required': False},
        }


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'role', 'avatar']

