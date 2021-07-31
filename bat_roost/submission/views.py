from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from submission.models import Submission, SubmissionImage
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import get_object_or_404
import csv
import json
from django.core.serializers import serialize
from core.permission import IsUserAdminTestMixin


class AllsubmissionDetails(IsUserAdminTestMixin, DetailView):
    model = Submission
    template_name = "submission/sub_det.html"
    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        pk  = self.kwargs.get('pk')
        context["markers"] = json.loads(serialize("geojson", Submission.objects.filter(pk=pk)))
        context["domain"] = self.request.META['HTTP_HOST']
        return context


class AllSubmissionView(IsUserAdminTestMixin, ListView):
    model = Submission
    paginate_by = 9
    template_name = 'submission/all_sub.html'

    # def get_queryset(self, *args, **kwargs):
    #     if self.request.GET.get('Accepted'):

    #         return Submission.objects.filter(status=Submission.ACCEPTED)

    #     elif self.request.GET.get('UnderReview'):
    #         return Submission.objects.filter(status=Submission.UNDER_REVIEW)
    #     return Submission.objects.all()


    def get_context_data(self, **kwargs):
        context = super(AllSubmissionView, self).get_context_data(**kwargs)
        #submission_list = self.get_queryset()
        submission_list =  Submission.objects.all()
        print(self.request.GET)
        if self.request.GET.get("status")=="Accepted":
            submission_list =  submission_list.filter(status=Submission.ACCEPTED)
        if self.request.GET.get("status")=="UnderReview":
            submission_list =  submission_list.filter(status=Submission.UNDER_REVIEW)
        pk = self.request.GET.get("pk")
        if  pk:
            submission_list = submission_list.filter(pk=pk)
        if self.request.GET.get("group1")=="st":
            submission_list = submission_list.order_by("submission_time")
        if self.request.GET.get("group1")=="pt":
            submission_list = submission_list.order_by("photo_taken_time")


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
    template_name = 'submission/sub_accept.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.ACCEPTED)


class ReviewSubmissionView(AllSubmissionView):
    template_name = 'submission/sub_ur.html'

    def get_queryset(self, *args, **kwargs):
        return Submission.objects.filter(status=Submission.UNDER_REVIEW)


class StatusView(IsUserAdminTestMixin, View):
    def get(self, request):
        obj = get_object_or_404(Submission, id=request.GET.get("id"))
        return JsonResponse({
            "id": obj.id,
            "status": obj.status,
            "status_options": Submission.STATUS_CHOICES,
        })

    def post(self, request):
        obj = get_object_or_404(Submission, id=request.POST.get("id"))
        status = request.POST.get("status")
        review = request.POST.get("review")
        if not Submission.is_valid_status(status):
            return JsonResponse({
                "success": False,
                "message": "Invalid status code",
            }, status=400)

        obj.status = status
        obj.review = review
        obj.save()
        return JsonResponse({
            "success": True,
            "status": obj.status,
            "status_display": obj.get_status_display(),
        })


def DownloadSubmission(request):
    items = Submission.objects.filter(status=Submission.ACCEPTED)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="submission.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['user', 'description', 'approx_bats',
                     'submission_time', 'photo_taken_time'])
    for obj in items:
        writer.writerow([obj.user, obj.description, obj.approx_bats,
                         obj.submission_time, obj.photo_taken_time])
    return response

class LocationView(TemplateView):
     model = Submission
     template_name = 'submission/loc.html'
     def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(serialize("geojson", Submission.objects.all()))
        context["domain"] = self.request.META['HTTP_HOST']
        return context
