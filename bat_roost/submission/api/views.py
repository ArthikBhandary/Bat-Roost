from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import exceptions, status

from submission.api.serializers import SubmissionSerializer, SubmissionDetailSerializer, SubmissionListSerializer, ImageSerializer
from submission.models import Submission, SubmissionImage

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from core.models import User
import csv

class SubmissionCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        print("Hello\n\n############")
        obj = serializer.save(user=User.objects.all()[0])
        id  =   obj.id
        print(id)
        print(obj)
        # converts querydict to original dict
        print(self.request.data)
        print([key for key in self.request.data])
        images = dict((self.request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(id,
                                                            img_name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
                arr.append(file_serializer.data)


class SubmissionListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)


class SubmissionDetailApiView(RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    def get_object(self):
        return get_object_or_404(Submission,pk=self.request.GET.get("pk"))



class SubmissionListDownloadApiView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Submission.objects.filter(status=Submission.ACCEPTED, user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submission.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['user', 'description', 'approx_bats',
                         'submission_time', 'photo_taken_time'])

        for obj in items:
            writer.writerow([obj.user, obj.description, obj.approx_bats,
                             obj.submission_time, obj.photo_taken_time])

        return response



class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, *args, **kwargs):
        property_id = request.data['submission_id']
        print(property_id)
        # converts querydict to original dict
        print(request.data)
        print([key for key in request.data])
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(property_id,
                                                            img_name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid(raise_e):
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)



def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['submission'] = property_id
    dict['image'] = image
    return dict
