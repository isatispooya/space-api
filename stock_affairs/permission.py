from rest_framework.permissions import BasePermission
from stock_affairs.models import Shareholders, Precedence, UnusedPrecedencePurchase, UnusedPrecedenceProcess

class IsShareholder(BasePermission):
    def has_permission(self, request, view):
        try:
            shareholder = Shareholders.objects.filter(name__user=request.user)
            return shareholder.exists()
        except:
            return False
        
class IsPrecedence(BasePermission):
    def has_permission(self, request, view):
        try:
            precedence = Precedence.objects.filter(position__user=request.user)
            return precedence.exists()
        except:
            return False

class IsUnusedPrecedencePurchase(BasePermission):
    def has_permission(self, request, view):
        try:
            unused_precedence_purchase = UnusedPrecedencePurchase.objects.filter(is_active=True, amount__gt=0)
            return unused_precedence_purchase.exists()
        except:
            return False

class IsUnusedPrecedenceProcess(BasePermission):
    def has_permission(self, request, view):
        try:
            unused_precedence_process = UnusedPrecedenceProcess.objects.filter(is_active=True, used_amount__gt=0)
            return unused_precedence_process.exists()
        except:
            return False
