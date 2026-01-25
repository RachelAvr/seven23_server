from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q

from seven23.models.accounts.user_files import UserFile
from seven23.models.accounts.serializers import UserFileSerializer
from seven23.api.accounts.utils import resolve_account_for_user  


class UserFileListCreateView(generics.ListCreateAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return UserFile.objects.filter(account__owner=user) | UserFile.objects.filter(account__guests__user=user)

    def perform_create(self, serializer):
        # print(self.request.data)
        account = resolve_account_for_user(self.request.user)
        #print(serializer.validated_data)
        serializer.save(account=account, uploaded_by=self.request.user)
        print(serializer.validated_data)

class UserFileRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return UserFile.objects.filter(account__owner=user) | UserFile.objects.filter(account__guests__user=user)
  

   
