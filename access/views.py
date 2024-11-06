from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Permission
from .serializer import PermissionSerializer
from rest_framework.response import Response
from user.models import User



class PermissionListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    



class SetUserPermissionView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        permissions_list  = request.data.get('permission_id')
        user = User.objects.get(id=user_id)
        user.user_permissions.clear()

        for permission_id in permissions_list:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.add(permission)
        user.save()
        return Response({"message": "Permission set successfully"})

