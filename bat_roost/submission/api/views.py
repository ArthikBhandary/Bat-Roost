import csv
import json

from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from submission.api.serializers import SubmissionSerializer, ImageCreateSerializer, SpeciesSerializer
from submission.models import Submission, Species


class SubmissionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        if "latitude" not in request.data or "longitude" not in request.data:
            return Response({"non_field_errors": "Position is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(request.data["latitude"].strip(" "))
            longitude = float(request.data["longitude"].strip(" "))
        except TypeError:
            return Response("Invalid Values for position", status=status.HTTP_400_BAD_REQUEST)

        species_id = []
        if self.request.data.get("species", ):
            try:
                species_list = json.loads(self.request.data.get("species", ))
                if type(species_list) is not list:
                    return Response("Invalid Values for species. Not a List", status=status.HTTP_400_BAD_REQUEST)

                species_id = [int(x) for x in species_list]
            except ValueError as e:
                print(e)
                return Response("Invalid Values for species", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, latitude=latitude,
                            longitude=longitude, species_id=species_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        print(self.request.data)
        serializer.is_valid(raise_exception=True)
        point = Point(x=kwargs["longitude"], y=kwargs["latitude"])
        obj = serializer.save(user=self.request.user, location=point)
        obj_id = obj.id
        images = dict(self.request.data.lists())['images']
        arr = []
        if kwargs.get("species_id"):
            species_id = kwargs["species_id"]
            current_specie = Species.objects.filter(pk__in=species_id)
            for specie in current_specie:
                obj.species.add(specie)

        for img_name in images:
            modified_data = modify_input_for_multiple_files(obj_id,
                                                            img_name)
            file_serializer = ImageCreateSerializer(data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
                arr.append(file_serializer.data)


class SubmissionListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)


class SpeciesApiView(ListAPIView):
    serializer_class = SpeciesSerializer
    pagination_class = None

    def get_queryset(self):
        return Species.objects.all()


class SubmissionDetailApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_object(self):
        return get_object_or_404(Submission, pk=self.request.GET.get("pk", ))


class SubmissionListDownloadApiView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        items = Submission.objects.filter(
            status=Submission.ACCEPTED, user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submission.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['user', 'description', 'approx_bats',
                         'submission_time', 'photo_taken_time'])

        for obj in items:
            writer.writerow([obj.user, obj.description, obj.approx_bats,
                             obj.submission_time, obj.photo_taken_time])

        return response


def modify_input_for_multiple_files(property_id, image):
    dict = {'submission': property_id, 'image': image}
    return dict
