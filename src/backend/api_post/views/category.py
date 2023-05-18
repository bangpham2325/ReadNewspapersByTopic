from api_base.views import BaseViewSet
from api_post.models import Category
from api_post.serializers import CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from api_auth.permissions import AdminPermission


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    permission_map = {
        "Create": [AdminPermission]
    }

    def list(self, request, *args, **kwargs):
        params = request.query_params
        search_query = params.get("q", "")
        res_data = Category.objects.filter(Q(title__icontains=search_query))
        page = self.paginate_queryset(res_data)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(res_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
