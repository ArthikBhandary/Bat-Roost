from django.urls import path
from submission.api.views import SubmissionListApiView, SubmissionCreateAPIView, SubmissionDetailApiView

app_name = "submission"


urlpatterns = [
    path("list/", SubmissionListApiView.as_view(), name="list"),
    path("create/", SubmissionCreateAPIView.as_view(), name="create"),
    path("details/", SubmissionDetailApiView.as_view(), name="details"),
]
