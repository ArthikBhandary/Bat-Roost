from django.shortcuts import render
from django.views.generic.base import TemplateView
from submission.models import Submission,SubmissionImage
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.

from core.permission import IsUserAdminTestMixin


class AllsubmissionDetails(DetailView):
    model = Submission
    template_name = "submission/sub_det.html"
    
 





class AllSubmissionView(IsUserAdminTestMixin, ListView):
    model = Submission
    paginate_by = 10

    template_name = 'submission/all_sub.html'

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


class AcceptedSubmissionView(AllSubmissionView):
    model = Submission
    template_name = 'submission/sub_accept.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.ACCEPTED)


class ReviewSubmissionView(AllSubmissionView):
    template_name = 'submission/sub_ur.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.UNDER_REVIEW)
