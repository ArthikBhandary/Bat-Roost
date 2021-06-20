from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from submission.api.serializers import SubmissionSerializer, SubmissionDetailSerializer, SubmissionListSerializer
from submission.models import Submission

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv

class SubmissionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubmissionListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)


class SubmissionDetailApiView(RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    def get_object(self):
        return get_object_or_404(Submission,pk=self.request.GET.get("pk"))



class SubmissionListDownloadApiView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Submission.objects.filter(status=Submission.ACCEPTED, user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submission.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['user', 'description', 'approx_bats',
                         'submission_time', 'photo_taken_time'])

        for obj in items:
            writer.writerow([obj.user, obj.description, obj.approx_bats,
                             obj.submission_time, obj.photo_taken_time])

        return response
