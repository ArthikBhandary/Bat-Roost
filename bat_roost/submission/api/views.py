from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from submission.api.serializers import SubmissionSerializer, SubmissionDetailSerializer
from submission.models import Submission


class SubmissionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionDetailSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)
