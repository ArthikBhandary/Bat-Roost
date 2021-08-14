from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from allauth.account.utils import send_email_confirmation
from rest_framework.permissions import IsAuthenticated
# from django.utils.translation import ugettext_lazy as _
# from rest_auth.views import LoginView
from core.api.serializers import UserDataSerializer
# from core.api.serializers import LoginApiSerializers
from core.models import User

# class EmailVerifiedPermission(BasePermission):
#     message = "Email is not verified"
#     def has_permission(self, request, view):
#         # print(request.user.is_verified)
#         print(request.user)
#         if request.method in SAFE_METHODS:
#             return True
#         if request.user.is_authenticated:
#             print(request.user.is_verified)
#             print("Hello")
#             if not request.user.is_verified:
#                 print(request.user.is_verified)
#                 return False
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         print("Hello")
#         return not obj.user.is_verified


class UserDataAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user



class EmailConfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_201_CREATED)

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)



class LoginApiView(LoginView):

    def post(self, request, *args, **kwargs):
        self.request = request
        try:
            if self.request.data.get("username"):
                user = User.objects.get(username=self.request.data["username"])
            elif self.request.data.get("email"):
                user = User.objects.get(email=self.request.data["email"])
            if not user.is_verified:
                send_email_confirmation(request, user)
                return Response({'non_field_errors': ['Email not Verified. Email confirmation sent']}, status=status.HTTP_403_FORBIDDEN)
        except:
            pass
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()
