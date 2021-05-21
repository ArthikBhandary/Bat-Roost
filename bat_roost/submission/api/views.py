from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from submission.api.serializers import SubmissionSerializer, SubmissionDetailSerializer, SubmissionListSerializer
from submission.models import Submission

from django.shortcuts import get_object_or_404

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
        print(self.request.GET.get("id"))
        return get_object_or_404(Submission,pk=self.request.GET.get("pk"))
