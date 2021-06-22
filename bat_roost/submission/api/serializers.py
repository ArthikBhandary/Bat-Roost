from rest_framework import serializers

from submission.models import Submission, SubmissionImage


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("description", "approx_bats", "photo_taken_time")


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time", "photo_taken_time")

class SubmissionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time", "photo_taken_time")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImage
        fields = (
            'submission',
            'image'
        )
