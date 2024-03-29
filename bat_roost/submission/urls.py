from django.urls import path, re_path
from django.conf.urls import url
from .views import AllSubmissionView, AcceptedSubmissionView, ReviewSubmissionView, \
                    AllSubmissionDetails, StatusView,DownloadSubmission,LocationView


app_name = "submission"

urlpatterns = [
    path('all/',AllSubmissionView.as_view(),name='AllSubmissionView'),
    path('accepted/', AcceptedSubmissionView.as_view(), name="AcceptedSubmissionView"),
    path('review/', ReviewSubmissionView.as_view(), name="ReviewSubmissionView"),
    url(r'^all/(?P<pk>\d+)/$', AllSubmissionDetails.as_view(), name='detail'),
    path('change_status/',StatusView.as_view(), name="status_update"),
    path('download/',DownloadSubmission,name='DownloadSubmission'),
    path("loc/",LocationView.as_view(),name="loc"),
    
]
