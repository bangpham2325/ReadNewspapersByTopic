from api_base.services import BaseService
from api_user.constants import Roles
from api_user.models import Account, User
from itertools import groupby
from api_base.services import CloudinaryService
from api_post.models import Category
from django.db.models.functions import ExtractMonth
from django.db.models import Count

MONTH_LIST = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10',
              'Tháng 11', 'Tháng 12']

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

    @classmethod
    def report_user_by_role(cls):
        user_reports = {}

        # Lấy danh sách user theo role và tháng
        users = User.objects.annotate(month=ExtractMonth('created_at')).filter(month__in=range(1, 13)).values('month',
                                                                                                              'role').annotate(
            count=Count('id')).order_by('role')

        # Tạo từ điển báo cáo user theo role và tháng
        for month in MONTH_LIST:
            user_report = {}
            for role in Roles.choices():
                user_data = next((user for user in users if
                                  user['role'] == role[0] and user['month'] == MONTH_LIST.index(month) + 1), None)
                count = user_data['count'] if user_data else 0
                user_report[role[1]] = count

            user_reports[month] = user_report

        return user_reports
