from rest_framework import serializers
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence

class ShareholdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shareholders
        fields = '__all__'

class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = '__all__'

class PrecedenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precedence
        fields = '__all__'

class CapitalIncreasePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalIncreasePayment
        fields = '__all__'

class DisplacementPrecedenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplacementPrecedence
        fields = '__all__'

