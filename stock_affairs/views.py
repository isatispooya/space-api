from django.shortcuts import render
from rest_framework import viewsets
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence
from rest_framework.permissions import IsAuthenticated , IsAdminUser 
from .serializers import ShareholdersSerializer , StockTransferSerializer , PrecedenceSerializer , CapitalIncreasePaymentSerializer , DisplacementPrecedenceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q




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

