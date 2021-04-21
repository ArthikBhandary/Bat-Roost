from django.urls import path, re_path

from core.views import AdminLoginView, ThanksView

app_name = "core"

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name="login"),
    path('thanks/', ThanksView.as_view(), name="thanks")
]
