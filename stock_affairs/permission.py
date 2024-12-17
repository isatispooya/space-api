from rest_framework.permissions import BasePermission
from stock_affairs.models import Shareholders, Precedence, UnusedPrecedencePurchase, UnusedPrecedenceProcess

class IsShareholder(BasePermission):
    def has_permission(self, request, view):
        shareholder = Shareholders.objects.filter(user=request.user)
        if shareholder.exists():
            return True
        else:
            return False
        
class IsPrecedence(BasePermission):
    def has_permission(self, request, view):
        precedence = Precedence.objects.filter(user=request.user)
        if precedence.exists():
            return True
        else:
            return False

class IsUnusedPrecedencePurchase(BasePermission):
    def has_permission(self, request, view):
        unused_precedence_purchase = UnusedPrecedencePurchase.objects.filter(is_active=True , amount__gt=0)
        if unused_precedence_purchase.exists():
            return True
        else:
            return False

class IsUnusedPrecedenceProcess(BasePermission):
    def has_permission(self, request, view):
        unused_precedence_process = UnusedPrecedenceProcess.objects.filter(is_active=True , amount__gt=0)
        if unused_precedence_process.exists():
            return True
        else:
            return False
