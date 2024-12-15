from django.shortcuts import render
from .models import UserLoginLog
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserLoginLogSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone
from rest_framework.views import APIView


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
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        # پیاده‌سازی منطق logout
        return Response({'message': 'Successfully logged out'})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # اضافه کردن لاگ
            UserLoginLog.objects.create(
                user=request.user,
                action='logout',
                status='success'
            )
            
            return Response(
                {"detail": "Successfully logged out"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid token"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        