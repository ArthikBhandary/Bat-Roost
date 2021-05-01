from django.urls import path

# from rest_auth.views import LoginView as LoginApiView
from core.api.views import LoginApiView
from core.api.views import UserDataAPIView


app_name = "core"


urlpatterns = [
    path("login/", LoginApiView.as_view(), name='api-login'),
    path("user/", UserDataAPIView.as_view(), name="api-details"),
]
