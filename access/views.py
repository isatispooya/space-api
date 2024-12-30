from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from django.contrib.auth.models import Permission
from .serializer import PermissionSerializer
from rest_framework.response import Response
from user.models import User
from stock_affairs.permission import IsUnusedPrecedenceProcess , IsPrecedence , IsShareholder , IsUnderwriting


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
            permissions = Permission.objects.filter(
                codename__in=[perm.split('.')[-1] for perm in permission_names]
            )
        else:
            permissions = user.user_permissions.all()
        unused_precedence_process_perm = IsUnusedPrecedenceProcess()
        precedence_perm = IsPrecedence()
        shareholder_perm = IsShareholder()
        underwriting_perm = IsUnderwriting()
        
        perm_data_unused_precedence_process = unused_precedence_process_perm.get_permission_data(request, self)
        perm_data_precedence = precedence_perm.get_permission_data(request, self)
        perm_data_shareholder = shareholder_perm.get_permission_data(request, self)
        perm_data_underwriting = underwriting_perm.get_permission_data(request, self)
        
        permissions = list(permissions)
        if perm_data_unused_precedence_process:
            permissions.append(perm_data_unused_precedence_process)
        if perm_data_precedence:
            permissions.append(perm_data_precedence)
        if perm_data_shareholder:
            permissions.append(perm_data_shareholder)
        if perm_data_underwriting:
            permissions.append(perm_data_underwriting)
    

        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
