from django.urls import path, include

from core.views import AdminLoginView, ThanksView, test_view

app_name = "core"

endpoint = "api/v1/"


urlpatterns = [
    path('login/', AdminLoginView.as_view(), name="login"),
    path('thanks/', ThanksView.as_view(), name="thanks"),
    path(endpoint, include('core.api.urls')),
    path(endpoint + "submission/", include('submission.api.urls')),
    path("test",test_view.as_view(), name="test")
]
