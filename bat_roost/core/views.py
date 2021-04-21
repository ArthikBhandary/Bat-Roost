from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import View

from core.models import User
from core.forms import AdminAuthForm

# Create your views here.
class AdminLoginView(LoginView):

    authentication_form = AdminAuthForm
    template_name = "core/admin_login.html"
    redirect_field_name = 'thanks/'


class ThanksView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Thanks")
