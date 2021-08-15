from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import AdminLoginView, ThanksView, EmailConfirmedView, download_users

app_name = "core"

endpoint = "api/v1/"


urlpatterns = [
    path('login/', AdminLoginView.as_view(), name="login"),
    path('thanks/', ThanksView.as_view(), name="thanks"),
    path(endpoint, include('core.api.urls')),
    path(endpoint + "submission/", include('submission.api.urls')),
    path("email_confirmed/",EmailConfirmedView.as_view(), name="email_confirmed"),
    path("download_user/",download_users, name="download_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
