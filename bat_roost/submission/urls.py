from django.urls import path, re_path
from .views import AllSubmissionView, RejectedSubmissionView, ReviewSubmissionView
app_name = "submission"

urlpatterns = [
    path('all/',AllSubmissionView.as_view(),name='all_submission'),
    path('rejected/', RejectedSubmissionView.as_view(), name="rejected_submission"),
    path('review/', ReviewSubmissionView.as_view(), name="review_submission"),
]
