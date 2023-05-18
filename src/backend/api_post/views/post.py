from api_base.views import BaseViewSet
from api_post.models import Posts
from api_post.serializers import PostSerializer, PostShortSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from api_auth.permissions import AdminPermission, UserPermission

from api_user.constants import Roles
from common.constants.api_constants import HttpMethod
from api_post.services import PostService, CrawlService
from api_interaction.models import Bookmark


class PostViewSet(BaseViewSet):
    queryset = Posts.objects.all()
    permission_class = [AllowAny]
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    permission_map = {
        "Create": [IsAdminUser],
        "get_post_management": [AdminPermission],
        "like_post": [IsAuthenticated],
        "list_bookmark": [IsAuthenticated],
        "update_list_status_post": [AdminPermission]

    }
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

    @action(methods=[HttpMethod.GET], detail=False, url_path="library", serializer_class=PostShortSerializer)
    def get_post_library(self, request, *args, **kwargs):
        res_data = PostService.get_list_post_by_favourite()
        serializer = {"post_favourite": self.get_serializer(res_data, many=True).data}
        res_data = PostService.get_list_post_by_views()
        serializer.update({"post_views": self.get_serializer(res_data, many=True).data})
        res_data = PostService.get_list_post_by_likes()
        serializer.update({"post_likes": self.get_serializer(res_data, many=True).data})
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="management", serializer_class=PostShortSerializer)
    def get_post_management(self, request, *args, **kwargs):
        user_obj = request.user.user
        params = request.query_params
        if user_obj.role == Roles.USER.value:
            res_data = PostService.get_post_management(params)
            page = self.paginate_queryset(res_data)

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(data=None, status=status.HTTP_200_OK)

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

    @action(methods=[HttpMethod.GET], detail=True, url_path="like_post", serializer_class=PostShortSerializer, permission_class=[IsAuthenticated])
    def like_post(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user.user in post.liked_by.all():
            return Response({'message': 'You have already liked this post!'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes += 1
        post.save()
        post.liked_by.add(request.user.user)
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="list_bookmark", serializer_class=PostShortSerializer)
    def list_bookmark(self, request, *args, **kwargs):
        bookmark = Bookmark.objects.filter(user_id=request.user.user.id)
        post_ids = [item[0] for item in list(bookmark.values_list('post_id'))]
        post = Posts.objects.filter(id__in=post_ids)
        serializer = self.get_serializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="create_post", serializer_class=PostShortSerializer)
    def create_post(self, request, *args, **kwargs):
        bookmark = CrawlService.thread_crawl()
        return Response(bookmark, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.PATCH], detail=False, url_path="publish_post", serializer_class=PostShortSerializer)
    def update_list_status_post(self, request, *args, **kwargs):
        post_ids = request.data.get('post_ids', [])
        PostService.update_status_post(post_ids)
        return Response({'message': 'Your changes have been saved.'}, status=status.HTTP_200_OK)
