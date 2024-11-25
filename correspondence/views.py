from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Correspondence
from .serializers import CorrespondenceSerializer

class CorrespondenceSenderViewset(viewsets.ModelViewSet):
    queryset = Correspondence.objects.all()
    serializer_class = CorrespondenceSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Correspondence.objects.filter(sender=self.request.user)

class CorrespondenceReceiverViewset(viewsets.ModelViewSet):
    serializer_class = CorrespondenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Correspondence.objects.filter(receiver=self.request.user)