from rest_framework import serializers

from submission.models import Submission, SubmissionImage, Species


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImage
        fields = ["submission", "image"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImage
        fields = ["image"]

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ("pk", "name")


class SubmissionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Submission
        fields = ("pk", "description", "approx_bats",
                  "photo_taken_time", "images",  "latitude", "longitude", "review")
        read_only_fields = ["pk", "images",  "latitude", "longitude", "review"]


class SubmissionListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time",
                  "photo_taken_time", "images", "latitude", "longitude", "review")
        read_only_fields = ["pk", "images", "review"]


class SubmissionDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    species = SpeciesSerializer(read_only=True, many=True)
    class Meta:
        model = Submission
        fields = ("pk", "status", "description", "approx_bats", "submission_time",
                  "photo_taken_time",  "images",  "latitude", "longitude", "review", "species")
        read_only_fields = ["pk", "images", "review", "species"]
