from django.shortcuts import render
from rest_framework import viewsets
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence , UnusedPrecedencePurchase , UnusedPrecedenceProcess
from rest_framework.permissions import IsAuthenticated , IsAdminUser 
from .serializers import ShareholdersSerializer , StockTransferSerializer , PrecedenceSerializer , CapitalIncreasePaymentSerializer , DisplacementPrecedenceSerializer , UnusedPrecedencePurchaseSerializer , UnusedPrecedenceProcessSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError




class ShareholdersViewset(viewsets.ModelViewSet):
    queryset = Shareholders.objects.all()
    serializer_class = ShareholdersSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif not self.request.user.is_staff:
            self.queryset = Shareholders.objects.filter(name__user=self.request.user)
        return super().get_permissions()
    

class StockTransferViewset(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif not self.request.user.is_staff:
            self.queryset = StockTransfer.objects.filter(
                Q(buyer__user=self.request.user) | Q(seller__user=self.request.user)
            )
        return super().get_permissions()


class PrecedenceViewset(viewsets.ModelViewSet):
    queryset = Precedence.objects.all()
    serializer_class = PrecedenceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CapitalIncreasePaymentViewset(viewsets.ModelViewSet):
    queryset = CapitalIncreasePayment.objects.all()
    serializer_class = CapitalIncreasePaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class DisplacementPrecedenceViewset(viewsets.ModelViewSet):
    queryset = DisplacementPrecedence.objects.all()
    serializer_class = DisplacementPrecedenceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# خرید از فرایند
class UnusedPrecedencePurchaseViewset(viewsets.ModelViewSet):
    queryset = UnusedPrecedencePurchase.objects.all()
    serializer_class = UnusedPrecedencePurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create' , 'list' , 'retrieve']:
            self.permission_classes = [IsAdminUser | IsAuthenticated]
        elif self.action in ['update' , 'partial_update' , 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def create(self, request):
        process_id = request.data.get('process')
        requested_amount = request.data.get('requested_amount')
        process = UnusedPrecedenceProcess.objects.get(id=process_id)
        # بررسی موجودی
        if requested_amount > process.used_amount:
            raise ValidationError({"error": "مقدار درخواستی بیشتر از موجودی است"})
        # محاسبه قیمت
        calculated_price = requested_amount * process.price

        # ساخت دیتای اولیه
        data = {
            'user': request.user.id,
            'process': process.id,
            'requested_amount': requested_amount,
            'amount': process.used_amount,
            'price': calculated_price,
            'status': 'pending'
        }

     
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user=self.request.user)
        
    
    
class UnusedPrecedenceProcessViewset(viewsets.ModelViewSet):
    queryset = UnusedPrecedenceProcess.objects.all()
    serializer_class = UnusedPrecedenceProcessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset()
