from rest_framework import serializers

from submission.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("description", "approx_bats", "submission_time", "")


class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("status","description", "approx_bats", "submission_time", "photo_taken_time")
