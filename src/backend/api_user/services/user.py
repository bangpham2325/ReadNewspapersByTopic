from api_base.services import BaseService
from api_user.constants import Roles
from api_user.models import Account, User
from itertools import groupby
from api_base.services import CloudinaryService
from api_post.models import Category


class UserService(BaseService):
    @classmethod
    def create_user(cls, validated_data):
        account = dict({
            # 'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        })
        if validated_data.get('role') is Roles.ADMIN.value:
            account = Account.objects.create_superuser(**account)
        elif validated_data.get('role') is Roles.USER.value:
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

    @classmethod
    def upload_avatar(cls, image):
        upload_data = CloudinaryService.upload_avatar_user_image(image)
        return upload_data.get("url")

    @classmethod
    def add_categories(cls, data, category_id):
        categories = Category.objects.filter(id__in=category_id)
        data.categories.set(categories)
        return data
