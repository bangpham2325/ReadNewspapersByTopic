from rest_framework_extensions.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from api_auth.views import *
from .views import GoogleSocialAuthView

app_name = "api_auth"
router = DefaultRouter()

_urlpatterns = [
    path("login/", csrf_exempt(login_view), name="login"),
    path(r"registers", csrf_exempt(register_user), name="register_user"),
    path(r"google/", csrf_exempt(GoogleSocialAuthView.as_view())),
]

urlpatterns = router.urls + _urlpatterns
