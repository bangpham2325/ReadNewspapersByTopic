import api_post
from api_base.views import BaseViewSet
from api_post.models import Posts
from api_post.serializers import PostSerializer, PostShortSerializer, PostLikeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q, Avg, Prefetch
from rest_framework import status
from rest_framework.decorators import action
from api_auth.permissions import AdminPermission, UserPermission, AuthorPermission
from api_interaction.serializers.bookmark import BookmarkSerializer
from django.utils.text import slugify

from api_user.constants import Roles
from common.constants.api_constants import HttpMethod
from api_post.services import PostService
from api_interaction.models import Bookmark, Comment, Rating


class PostViewSet(BaseViewSet):
    queryset = Posts.objects.all()
    permission_class = [AllowAny]
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    permission_map = {
        "create": [AuthorPermission, IsAdminUser],
        "get_post_management": [AdminPermission],
        "like_post": [IsAuthenticated],
        "list_bookmark": [IsAuthenticated],
        "update_list_status_post": [AdminPermission],
        "add_bookmark": [IsAuthenticated],
        "get_post_by_author": [AllowAny],
        "get_post_management_by_author": [AdminPermission],
        "list_post_by_author": [AuthorPermission],

    }
    serializer_map = {
        "list": PostShortSerializer,
    }

    def retrieve(self, request, *args, **kwargs):
        instance = Posts.objects.select_related('category', 'source').prefetch_related(
                        Prefetch('post_rating', queryset=Rating.objects.select_related('user')),
                        Prefetch('post_comment', queryset=Comment.objects.select_related('user').prefetch_related(
                            Prefetch('child_comments', queryset=Comment.objects.select_related('user'))
                        )),
                        Prefetch('post_bookmark', queryset=Bookmark.objects.select_related('user'))
                    )\
            .prefetch_related('contents', 'keywords').get(id=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        params = request.query_params
        if request.user.id is not None:
            category_ids = request.user.user.categories.values_list('id', flat=True)
        else:
            category_ids = None
        res_data = PostService.get_list_post_by_category(params, category_ids)
        page = self.paginate_queryset(res_data)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(res_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="library", serializer_class=PostShortSerializer)
    def get_post_library(self, request, *args, **kwargs):
        params = request.query_params
        if request.user.id is not None:
            category_ids = request.user.user.categories.values_list('id', flat=True)
        else:
            category_ids = None
        res_data = PostService.get_list_post_by_favourite(category_ids)
        serializer = {"post_favourite": self.get_serializer(res_data, many=True).data}
        res_data = PostService.get_list_post_by_views(category_ids)
        serializer.update({"post_views": self.get_serializer(res_data, many=True).data})
        res_data = PostService.get_list_post_by_likes(category_ids)
        serializer.update({"post_likes": self.get_serializer(res_data, many=True).data})
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="management", serializer_class=PostShortSerializer)
    def get_post_management(self, request, *args, **kwargs):
        user_obj = request.user.user
        params = request.query_params
        if user_obj.role == Roles.ADMIN.value:
            res_data = PostService.get_post_management(params)
            page = self.paginate_queryset(res_data)

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(data=None, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=True, url_path="like_post", serializer_class=PostLikeSerializer)
    def like_post(self, request, *args, **kwargs):
        post = self.get_object()
        status_like = False
        if request.user.user in post.liked_by.all():
            post.likes -= 1
            post.save()
            post.liked_by.remove(request.user.user)
        else:
            post.likes += 1
            status_like = True
            post.save()
            post.liked_by.add(request.user.user)
        serializer = self.get_serializer(post)
        return Response({"likes": serializer.data['likes'], "status": status_like}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="list_bookmark", serializer_class=PostShortSerializer)
    def list_bookmark(self, request, *args, **kwargs):
        bookmark = Bookmark.objects.filter(user_id=request.user.user.id)
        post_ids = [item[0] for item in list(bookmark.values_list('post_id'))]
        post = Posts.objects.filter(id__in=post_ids).prefetch_related('category').prefetch_related('source').prefetch_related('post_rating'
        ).annotate(avg_rating=Avg("post_rating__star_rating"))
        serializer = self.get_serializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.PATCH], detail=False, url_path="publish_post")
    def update_list_status_post(self, request, *args, **kwargs):
        post_ids = request.data.get('post_ids', [])
        PostService.update_status_post(post_ids)
        return Response({'message': 'Your changes have been saved.'}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=True, url_path="add_bookmark", serializer_class=BookmarkSerializer)
    def add_bookmark(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        bookmark = Bookmark.objects.filter(user_id=request.user.user.id, post_id=kwargs['pk'])
        if bookmark.exists():
            self.perform_destroy(bookmark)
            return Response({'message': 'you have deleted bookmarks for this post!', "status": False}, status=status.HTTP_200_OK)
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'message': 'you have added bookmarks for this post!', "status": True}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=True, url_path="recommend", serializer_class=PostShortSerializer)
    def recommend(self, request, *args, **kwargs):
        data = api_post.services.recommendation.get_recommendations(kwargs['pk'])
        serializer = self.get_serializer(data, many=True)
        return Response({'message': serializer.data})

    @action(methods=[HttpMethod.GET], detail=False, url_path="new_post", serializer_class=PostShortSerializer)
    def get_new_post(self, request, *args, **kwargs):
        params = request.query_params
        if request.user.id is not None:
            category_ids = request.user.user.categories.values_list('id', flat=True)
        else:
            category_ids = None
        res_data = PostService.get_list_new_post(params, category_ids)
        page = self.paginate_queryset(res_data)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(res_data, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="list_blog", serializer_class=PostShortSerializer)
    def get_list_blog(self, request, *args, **kwargs):
        params = request.query_params
        res_data = PostService.list_blog(params)
        page = self.paginate_queryset(res_data)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(res_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="get_post_by_author", serializer_class=PostShortSerializer)
    def get_post_by_author(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        res_data = PostService.get_post_by_author(user_id)
        serializer = self.get_serializer(res_data, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="management_author", serializer_class=PostShortSerializer)
    def get_post_management_by_author(self, request, *args, **kwargs):
        user_obj = request.user.user
        params = request.query_params
        if user_obj.role == Roles.ADMIN.value:
            res_data = PostService.get_post_management_author(params)
            page = self.paginate_queryset(res_data)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(data=None, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False, url_path="my_posts", serializer_class=PostShortSerializer)
    def list_my_post(self, request, *args, **kwargs):
        user_obj = request.user.user
        params = request.query_params
        if user_obj.role == Roles.AUTHOR.value:
            res_data = PostService.list_my_post(params, user_obj.id)
            page = self.paginate_queryset(res_data)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(data=None, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=True, lookup_field="slug", url_path="content",
            serializer_class=PostSerializer)
    def slug(self, request, *args, **kwargs):
        instance = Posts.objects.select_related('category', 'source').prefetch_related(
                        Prefetch('post_rating', queryset=Rating.objects.select_related('user')),
                        Prefetch('post_comment', queryset=Comment.objects.select_related('user').prefetch_related(
                            Prefetch('child_comments', queryset=Comment.objects.select_related('user'))
                        )),
                        Prefetch('post_bookmark', queryset=Bookmark.objects.select_related('user'))
                    )\
            .prefetch_related('contents', 'keywords').get(slug=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
