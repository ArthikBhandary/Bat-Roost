from django.shortcuts import render
from submission.models import Submission,SubmissionImage
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.

from core.permission import IsUserAdminTestMixin

class AllSubmissionView(IsUserAdminTestMixin, ListView):
    model = Submission
    paginate_by = 10

    template_name = 'submission/submit.html'

    def get_context_data(self, **kwargs):
        context = super(AllSubmissionView, self).get_context_data(**kwargs)
        submission_list = self.get_queryset()
        paginator = Paginator(submission_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            Submissions = paginator.page(page)
        except PageNotAnInteger:
            Submissions = paginator.page(1)
        except EmptyPage:
            Submissions = paginator.page(paginator.num_pages)

        context['submission_list'] = Submissions
        return context


class RejectedSubmissionView(AllSubmissionView):
    template_name = 'submission/submit.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.REJECTED)


class ReviewSubmissionView(AllSubmissionView):
    template_name = 'submission/submit.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.UNDER_REVIEW)
