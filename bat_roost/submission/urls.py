from django.urls import path, re_path
from .views import AllSubmissionView, AcceptedSubmissionView, ReviewSubmissionView
app_name = "submission"

urlpatterns = [
    path('all/',AllSubmissionView.as_view(),name='AllSubmissionView'),
    path('accepted/', AcceptedSubmissionView.as_view(), name="AcceptedSubmissionView"),
    path('review/', ReviewSubmissionView.as_view(), name="ReviewSubmissionView"),
]
