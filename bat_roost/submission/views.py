from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from submission.models import Submission, SubmissionImage, Species
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
from core.misc_functions import is_int_convertible


class AllsubmissionDetails(IsUserAdminTestMixin, DetailView):
    model = Submission
    template_name = "submission/sub_det.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context["markers"] = json.loads(serialize("geojson", Submission.objects.filter(pk=pk)))
        context["domain"] = self.request.META['HTTP_HOST']
        return context


class AllSubmissionView(IsUserAdminTestMixin, ListView):
    model = Submission
    paginate_no = 10
    template_name = 'submission/all_sub.html'

    def get_context_data(self, **kwargs):
        search_params = ""
        context = super(AllSubmissionView, self).get_context_data(**kwargs)
        # submission_list = self.get_queryset()
        submission_list = Submission.objects.all()
        context["filter_status"] = self.request.GET.get("status")
        if self.request.GET.get("status") == "Accepted":
            submission_list = submission_list.filter(status=Submission.ACCEPTED)
            search_params += "status=Accepted&"
        if self.request.GET.get("status") == "UnderReview":
            submission_list = submission_list.filter(status=Submission.UNDER_REVIEW)
            search_params += "status=UnderReview&"
        pk = self.request.GET.get("pk")
        if is_int_convertible(pk):
            submission_list = submission_list.filter(user__pk=pk)
            context["filter_pk"] = pk
            search_params += ("pk=" + pk + "&")
        group1 = self.request.GET.get("group1")
        context["filter_group1"] = group1
        if group1:
            search_params += "group1={param}&".format(param=group1)
            if group1 == "st":
                submission_list = submission_list.order_by("submission_time")
            if group1 == "pt":
                submission_list = submission_list.order_by("photo_taken_time")

        species_id = self.request.GET.get("species")
        if is_int_convertible(species_id):
            submission_list = submission_list.filter(species__id=species_id)
            context["species"] = species_id
            search_params += "species={param}&".format(param=species_id)
        context["search_params"] = search_params
        context["species_list"] = Species.objects.all()

        paginator = Paginator(submission_list, self.paginate_no)
        if paginator.num_pages > 1:
            context["is_paginated"] = True
        page = self.request.GET.get('page')
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)

        context['submission_list'] = submissions
        context['page_obj'] = submissions
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
    submission_list = Submission.objects.all()
    if request.GET.get("status") == "Accepted":
        submission_list = submission_list.filter(status=Submission.ACCEPTED)
    if request.GET.get("status") == "UnderReview":
        submission_list = submission_list.filter(status=Submission.UNDER_REVIEW)
    pk = request.GET.get("pk")
    if is_int_convertible(pk):
        submission_list = submission_list.filter(user__pk=pk)
    if request.GET.get("group1") == "st":
        submission_list = submission_list.order_by("submission_time")
    if request.GET.get("group1") == "pt":
        submission_list = submission_list.order_by("photo_taken_time")
    species_id = request.GET.get("species")
    if is_int_convertible(species_id):
        submission_list = submission_list.filter(species__id=species_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="submission.csv"'
    writer = csv.writer(response, delimiter=',')

    writer.writerow(['user', 'description', 'approx_bats',
                     'submission_time', 'photo_taken_time', 'status', 'latitude', 'longitude', 'species', 'image1',
                     'image2', 'image3', 'image4', 'image5'])
    for obj in submission_list:
        species_string = ", ".join(str(specie.name) for specie in obj.species.all())

        row_to_add = [obj.user, obj.description, obj.approx_bats,
                      obj.submission_time, obj.photo_taken_time, obj.status, obj.latitude, obj.longitude,
                      species_string]
        for image in obj.images.all():
            row_to_add.append(request.build_absolute_uri(image.image.url))
        writer.writerow(row_to_add)
    return response


class LocationView(TemplateView):
    model = Submission
    template_name = 'submission/loc.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        submission_list = Submission.objects.all()
        if self.request.GET.get("status") == "Accepted":
            submission_list = submission_list.filter(status=Submission.ACCEPTED)
        if self.request.GET.get("status") == "UnderReview":
            submission_list = submission_list.filter(status=Submission.UNDER_REVIEW)
        pk = self.request.GET.get("pk")
        if is_int_convertible(pk):
            submission_list = submission_list.filter(user__pk=pk)
        group1 = self.request.GET.get("group1")
        if group1:
            if group1 == "st":
                submission_list = submission_list.order_by("submission_time")
            if group1 == "pt":
                submission_list = submission_list.order_by("photo_taken_time")

        species_id = self.request.GET.get("species")
        if is_int_convertible(species_id):
            submission_list = submission_list.filter(species__id=species_id)
        context["markers"] = json.loads(serialize("geojson", submission_list))
        context["domain"] = self.request.META['HTTP_HOST']
        return context
