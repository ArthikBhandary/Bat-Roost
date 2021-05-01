from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView

from core.models import User
from core.forms import AdminAuthForm

# Create your views here.
class AdminLoginView(LoginView):

    authentication_form = AdminAuthForm
    template_name = "core/admin_login.html"


class ThanksView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Thanks " + request.user.username)


class test_view(TemplateView):
    template_name="test.html"

    def get_context_data(self, **kwargs):
        context = super(test_view, self).get_context_data(**kwargs)
        context.update({
            "test":"yeah"
        })
        return context
