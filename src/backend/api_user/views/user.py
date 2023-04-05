from api_auth.serializers import RegisterSerializer
from api_base.views import BaseViewSet
from api_user.models import User
from api_user.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from api_auth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated, AllowAny

from api_user.services import UserService


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    permission_map = {
        "retrieve": [IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                user = UserService.create_user(validated_data)
                return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            obj_users = UserService.get_all_users()
            res_data = dict()
            for user in obj_users:
                res_data.update({user[0]: self.serializer_class(user[1], many=True).data})
            return Response(res_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
