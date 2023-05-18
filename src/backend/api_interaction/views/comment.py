from rest_framework.response import Response
from api_base.views import BaseViewSet
from api_interaction.models import Comment
from api_post.models import Posts
from api_interaction.serializers import CommentSerializer, CommentPostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_map = {
        "list": CommentPostSerializer,
        "retrieve": CommentPostSerializer,
    }
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        comment = self.get_serializer(data=request.data)

        try:
            if comment.is_valid(raise_exception=True):
                self.perform_create(comment)
                headers = self.get_success_headers(comment.data)

            return Response(comment.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
