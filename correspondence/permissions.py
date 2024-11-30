from rest_framework.permissions import BasePermission


class IsReceiverCorrespondence(BasePermission):
    print('obj.receiver_internal')
    def has_object_permission(self, request, view, obj):
        return obj.receiver_internal == request.user
    
class IsSenderCorrespondence(BasePermission):
    print('sender'*10)
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user

class IsOpenCorrespondence(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.draft

