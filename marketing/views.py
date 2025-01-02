from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import InvitationCode, Invitation
from .serializers import InvitationCodeSerializer, InvitationSerializer
import random
import string

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            serializer = self.serializer_class(notification, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Notification.DoesNotExist:
            return Response(
                {"error": "نوتیفیکیشن مورد نظر یافت نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class InvitationCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        invitation_code = InvitationCode.objects.filter(introducer_user=user)
        if invitation_code.exists():
            serializer = InvitationCodeSerializer(invitation_code, many=True)
            return Response(serializer.data)
        else:
            characters = string.ascii_letters + string.digits
            code = ''.join(random.choices(characters, k=6))
            description = request.data.get('description', '')
            invitation_code = InvitationCode.objects.create(
                introducer_user=user, 
                code=code,
                description=description
            )
            serializer = InvitationCodeSerializer(invitation_code)
            return Response(serializer.data)

    def post(self, request):
        user = request.user
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choices(characters, k=6))
        description = request.data.get('description', '')
        invitation_code = InvitationCode.objects.create(introducer_user=user, code=code , description=description)
        serializer = InvitationCodeSerializer(invitation_code)
        return Response(serializer.data)

class InvitationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        invitation_codes = InvitationCode.objects.filter(introducer_user=user)
        if not invitation_codes.exists():
            return Response(
                {"message": "هیچ کد معرفی یافت نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        result = []
        for code in invitation_codes:
            invitations = Invitation.objects.filter(invitation_code=code)
            code_data = InvitationCodeSerializer(code).data
            code_data['invitations'] = InvitationSerializer(invitations, many=True).data
            result.append(code_data)
        
        return Response(result)
    