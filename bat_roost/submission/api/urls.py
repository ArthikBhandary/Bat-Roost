from django.urls import path
from submission.api import views

app_name = "submission"


urlpatterns = [
    path("list/", views.SubmissionListApiView.as_view(), name="list"),
    path("create/", views.SubmissionCreateAPIView.as_view(), name="create"),
    path("details/", views.SubmissionDetailApiView.as_view(), name="details"),
    path("download/", views.SubmissionListDownloadApiView.as_view(), name="details"),
]
