from django.shortcuts import render
from .models import Announcement , ShortCut
from rest_framework import viewsets
from rest_framework.permissions import AllowAny , IsAdminUser
from .serializers import AnnouncementSerializer , ShortCutSerializer

class AnnouncementView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class ShortCutView(viewsets.ModelViewSet):
    queryset = ShortCut.objects.all()
    serializer_class = ShortCutSerializer
    permission_classes = [AllowAny] 

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    

