from api_base.views import BaseViewSet
from api_post.models import Posts
from api_post.serializers import PostSerializer, PostShortSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from common.constants.api_constants import HttpMethod
from api_post.services import PostService


class PostViewSet(BaseViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_class = IsAuthenticated
    # permission_map = {
    #     "Create": [IsAdminUser]
    # }
    serializer_map = {
        "list": PostShortSerializer,
    }

    def list(self, request, *args, **kwargs):
        params = request.query_params
        res_data = PostService.get_list_post_by_category(params)
        page = self.paginate_queryset(res_data)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(res_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="post_filter_list", serializer_class=PostShortSerializer)
    def post_filter_list(self, request, *args, **kwargs):
        params = request.query_params
        res_data = PostService.get_list_post(params)
        page = self.paginate_queryset(res_data)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(res_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
