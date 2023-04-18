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
from api_interaction.models import Bookmark


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

    @action(methods=[HttpMethod.PUT], detail=True, url_path="like_post", serializer_class=PostShortSerializer)
    def liked_post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_pk')
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
