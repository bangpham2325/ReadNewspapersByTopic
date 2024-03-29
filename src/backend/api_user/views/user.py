from api_auth.serializers import RegisterSerializer
from api_base.views import BaseViewSet
from api_user.models import User
from api_user.serializers import UserSerializer, UserShortWithEmailSerializer
from rest_framework import status
from rest_framework.response import Response
from api_auth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import action
from api_user.services import UserService
from common.constants.api_constants import HttpMethod
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    permission_map = {
        "retrieve": [IsAuthenticated],
        "add_category": [IsAuthenticated],
        "update_avatar": [IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                user = UserService.create_user(validated_data)
                return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            obj_users = UserService.get_all_users()
            res_data = dict()
            for user in obj_users:
                res_data.update({user[0]: self.serializer_class(user[1], many=True).data})
            return Response(res_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.PATCH], detail=False, url_path="update_avatar", serializer_class=UserSerializer)
    def update_avatar(self, request, *args, **kwargs):
        account = request.user
        instance = User.objects.filter(account=account).first()
        avatar = request.FILES.get('avatar')
        avatar_link = UserService.upload_avatar(avatar)
        request.data['avatar'] = avatar_link
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Your changes have been saved.'}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.PATCH], detail=False, url_path="update_category", serializer_class=UserSerializer)
    def add_category(self, request, *args, **kwargs):
        account = request.user
        instance = User.objects.filter(account=account).first()
        category_ids = request.data.get('category_ids', [])
        UserService.add_categories(instance, category_ids)
        return Response({'message': 'Your changes have been saved.'}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.PATCH], detail=False, url_path="change_password", serializer_class=UserSerializer)
    def change_password(self, request, *args, **kwargs):
        account = request.user
        if account:
            if check_password(request.data["old_password"], account.password):
                account.password = make_password(request.data["new_password"])
                account.save()
                return Response({'success': True, 'message': 'Changed password successfully!'}, status=status.HTTP_200_OK)
        return Response({"details": "Incorrect username! Change password unsuccessfully."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False, url_path="admin_report_user", serializer_class=UserShortWithEmailSerializer)
    def admin_report_user(self, request, *args, **kwargs):
        user = User.objects
        params = request.query_params
        report_data = {}
        report = UserService.report_user_by_role()
        report_data.update({"report": report})
        search_role = request.query_params.get("role", "")
        search_query = request.query_params.get("q", "")
        rest_data = user.filter(Q(full_name__icontains=search_query) and Q(role__icontains=search_role)).order_by("role")
        page = self.paginate_queryset(rest_data)
        if page is not None:
            rest_data = page
            ordering = request.query_params.get('ordering')
            if ordering is not None:
                try:
                    if ordering.startswith("-"):
                        ordering = ordering[1:]
                        rest_data = sorted(page, key=lambda d: getattr(d, ordering), reverse=False)
                    else:
                        rest_data = sorted(page, key=lambda d: getattr(d, ordering), reverse=True)
                except:
                    pass
            serializer = self.get_serializer(rest_data, many=True)
            report_data['users'] = serializer.data
            return self.get_paginated_response(report_data)
        users = self.get_serializer(report, many=True).data
        report_data['users'] = users
        return Response(report, status=status.HTTP_200_OK)
