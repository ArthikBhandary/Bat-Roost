from django.urls import path, re_path
from .views import SubmissionView
app_name = "submission"

urlpatterns = [
    path('',SubmissionView.as_view(),name='submission'),
]
