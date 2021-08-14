from django.urls import path

from core.api.views import UserDataAPIView, EmailConfirmationAPIView, LoginApiView


app_name = "core"


urlpatterns = [
    path("login/", LoginApiView.as_view(), name='api-login'),
    path("user/", UserDataAPIView.as_view(), name="api-details"),
    path("email_confirmation/", EmailConfirmationAPIView.as_view(), name="api-confirm-email")
]
