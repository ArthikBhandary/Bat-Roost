from django.urls import path, include

from core.views import AdminLoginView, ThanksView

app_name = "core"

endpoint = "api/v1/"


urlpatterns = [
    path('login/', AdminLoginView.as_view(), name="login"),
    path('thanks/', ThanksView.as_view(), name="thanks"),
    path(endpoint, include('core.api.urls')),
]
