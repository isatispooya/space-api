from rest_framework import serializers
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence , UnusedPrecedencePurchase , UnusedPrecedenceProcess

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

class UnusedPrecedencePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnusedPrecedencePurchase
        fields = '__all__'

class UnusedPrecedenceProcessSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    
    class Meta:
        model = UnusedPrecedenceProcess
        fields = '__all__'
