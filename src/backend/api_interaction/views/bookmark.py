from django.db.models import Q

from api_base.views import BaseViewSet
from api_interaction.models import Bookmark
from api_interaction.serializers.bookmark import BookmarkSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class BookmarkViewSet(BaseViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bookmark = Bookmark.objects.filter(user_id=request.user.user.id, post_id=kwargs['post_pk'])
        if bookmark.exists():
            self.perform_destroy(bookmark)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
