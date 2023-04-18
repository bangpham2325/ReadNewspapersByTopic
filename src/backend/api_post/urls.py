from rest_framework_extensions.routers import DefaultRouter
from django.urls import path, include
from api_post.views import PostViewSet, CategoryViewSet, SourceViewSet
from api_interaction.views import RatingViewSet, CommentViewSet, BookmarkViewSet
from rest_framework_nested import routers

app_name = "api_post"
router = DefaultRouter()
router.register(r'source', SourceViewSet, basename='source')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'post', PostViewSet, basename='post')

post_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
post_router.register(r'ratings', RatingViewSet, basename='rating')
post_router.register(r'comments', CommentViewSet, basename='comment')
post_router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(post_router.urls)),
]