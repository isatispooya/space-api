from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from .permissions import IsSenderCorrespondence, IsReceiverCorrespondence, IsOpenCorrespondence
from .models import Correspondence
from .serializers import CorrespondenceSerializer
from .number_generator import CorrespondenceNumberGenerator
from django.db.models import Q

class CorrespondencerViewset(viewsets.ModelViewSet):
    queryset = Correspondence.objects.all()
    serializer_class = CorrespondenceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            if self.request.user.is_staff:
                self.permission_classes = [IsAuthenticated]
            else:
                self.permission_classes = [IsReceiverCorrespondence, IsSenderCorrespondence]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser & IsOpenCorrespondence, IsSenderCorrespondence & IsOpenCorrespondence]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(draft=True, number=None)
        
    def perform_update(self, serializer):
        obj = serializer.instance
        if obj.draft:
            number = CorrespondenceNumberGenerator.generate_number()[0]
            serializer.save(draft=False, number=number)
        else:
            serializer.save()
        


