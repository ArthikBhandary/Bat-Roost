"""bat_roost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from allauth.account.views import confirm_email, email_verification_sent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submission/', include('submission.urls')),
    path('forgot_password/', PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('', include('core.urls')),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path(
        "confirm-email/",
        email_verification_sent,
        name="account_email_verification_sent",
    ),
]
