from django.shortcuts import render
from .models import UserLoginLog
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserLoginLogSerializer

class UserLoginLogView(viewsets.ModelViewSet):
    queryset = UserLoginLog.objects.all()
    serializer_class = UserLoginLogSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'create', 'partial_update']:
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAdminUser]  
        return [permission() for permission in permission_classes]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserLoginLog.objects.all()
        return UserLoginLog.objects.filter(user=self.request.user)
