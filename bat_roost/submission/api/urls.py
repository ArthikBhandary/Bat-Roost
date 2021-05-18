from django.urls import path
from submission.api.views import SubmissionListApiView

app_name = "submission"


urlpatterns = [
    path("list/", SubmissionListApiView.as_view(), name="list"),
]
