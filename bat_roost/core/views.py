import csv

from core.forms import AdminAuthForm
from core.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView
from submission.models import Submission


# Create your views here.
class AdminLoginView(LoginView):
    authentication_form = AdminAuthForm
    template_name = "core/admin_login.html"


class ThanksView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Thanks " + request.user.username)


class EmailConfirmedView(TemplateView):
    template_name = "core/email_confirmed.html"


def download_users(request):
    user_list = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="submission.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['id', 'email', 'first_name', 'last_name',
                     'is_admin', 'contact_no', 'locality', 'is_verified', 'submissions', 'accepted', 'rejected'])
    for obj in user_list:
        submission_list = obj.submission_set.all()
        total_count = submission_list.count()
        accepted_count = submission_list.filter(status=Submission.ACCEPTED).count()
        rejected_count = submission_list.filter(status=Submission.REJECTED).count()
        row_to_add = [obj.pk, obj.email, obj.first_name, obj.last_name, obj.is_admin, obj.contact_no, obj.locality,
                      obj.is_verified, total_count, accepted_count, rejected_count]
        writer.writerow(row_to_add)
    return response
