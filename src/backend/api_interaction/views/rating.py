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
