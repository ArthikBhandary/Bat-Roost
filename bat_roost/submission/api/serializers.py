from rest_framework import serializers

from submission.models import Submission, SubmissionImage


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImage
        fields = ["submission", "image"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImage
        fields = ["image"]


class SubmissionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True,many=True)
    class Meta:
        model = Submission
        fields = ("pk", "description", "approx_bats", "photo_taken_time", "images")
        read_only_fields = ["pk", "images"]


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time", "photo_taken_time")


class SubmissionDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True,many=True)
    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time", "photo_taken_time",  "images",)
