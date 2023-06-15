from api_base.permission import MyBasePermission
from api_user.constants import Roles


class AdminPermission(MyBasePermission):
    match_any_roles = [Roles.ADMIN.value]


class UserPermission(MyBasePermission):
    match_any_roles = [Roles.USER.value]


class AuthorPermission(MyBasePermission):
    match_any_roles = [Roles.AUTHOR.value]


class AuthorOrAdminPermission(MyBasePermission):
    match_any_roles = [Roles.AUTHOR.value, Roles.ADMIN.value]
