from django.shortcuts import render
from submission.models import Submission,SubmissionImage
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.
class SubmissionView(ListView):
    model = Submission
    paginate_by = 1
  
    template_name = 'submission/submit.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionView, self).get_context_data(**kwargs) 
        submission_list = Submission.objects.all()
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
    

    