from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
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


class PermissionListForUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_superuser or user.is_staff:
            permission_names = user.get_all_permissions()
            """
                این خط دسترسی‌های کاربر را به صورت کد نام فیلتر می‌کند
                permission_names شامل دسترسی‌ها به فرمت "app_label.codename" است
                با split('.') آن را جدا کرده و آخرین بخش که همان codename است را برمی‌داریم

            """
            permissions = Permission.objects.filter(
                codename__in=[perm.split('.')[-1] for perm in permission_names]
            )
        else:
            permissions = user.user_permissions.all()
        
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
