from django.db.models import Q

from api_base.views import BaseViewSet
from api_interaction.models import Rating
from api_interaction.serializers import RatingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RatingViewSet(BaseViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        rating = Rating.objects.filter(Q(user_id=request.user.user.id) & Q(post_id=kwargs.get('post_pk')))
        if rating.exists():
            return Response({"detail": "you have created rating "}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
