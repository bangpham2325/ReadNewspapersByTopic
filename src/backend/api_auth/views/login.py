from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import check_password
from rest_framework import views, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api_auth.services import AccountService
from api_user.models import Account, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from api_auth.serializers import GoogleSocialAuthSerializer


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Type your email', default='admin@gmail.com'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Type your password', default='123456'),
    })
 )
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    password = request.data.get("password")
    email = request.data.get("email")
    account = Account.objects.filter(Q(email=email))
    if account.exists():
        account = account.first()
        if check_password(password, account.password):
            token = RefreshToken.for_user(account)
            response = {
                'user_id': account.user.id,
                'full_name': account.user.full_name,
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
            return Response(response)

    return Response({"details": "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(self.serializer_class(data).data, status=status.HTTP_200_OK)

