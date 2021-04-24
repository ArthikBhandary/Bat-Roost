from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import UserDataSerializer
from core.models import User

class UserDataAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user
