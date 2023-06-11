from api_auth.serializers import RegisterSerializer
from api_user.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'full_name': openapi.Schema(type=openapi.TYPE_STRING, default='User'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, default='user@gmail.com'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, default='', format='password'),
    })
 )
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register_user(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    try:
        if serializer.is_valid(raise_exception=True):
            res_data = serializer.save()
            return Response(UserSerializer(res_data).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'full_name': openapi.Schema(type=openapi.TYPE_STRING, default='Author'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, default='author@gmail.com'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, default='', format='password'),
    })
 )
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register_author(request):
    request.parser_context.get('view').action = 'author'
    serializer = RegisterSerializer(data=request.data, context=request.parser_context)
    try:
        if serializer.is_valid(raise_exception=True):
            res_data = serializer.save()
            return Response(UserSerializer(res_data).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

