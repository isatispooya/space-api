from rest_framework import serializers
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence , Underwriting , UnusedPrecedenceProcess
from companies.serializers import CompanySerializer
from user.serializers import UserSerializer
class ShareholdersSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Shareholders
        fields = '__all__'

class StockTransferSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    company_detail = CompanySerializer(source='company', read_only=True)
    buyer_detail = UserSerializer(source='buyer', read_only=True)
    seller_detail = UserSerializer(source='seller', read_only=True)
    class Meta:
        model = StockTransfer
        fields = '__all__'

class PrecedenceSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Precedence
        fields = '__all__'

class CapitalIncreasePaymentSerializer(serializers.ModelSerializer):
    precedence = PrecedenceSerializer(read_only=True)
    
    class Meta:
        model = CapitalIncreasePayment
        fields = '__all__'

class DisplacementPrecedenceSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    buyer_detail = UserSerializer(source='buyer', read_only=True)
    seller_detail = UserSerializer(source='seller', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = DisplacementPrecedence
        fields = '__all__'

class UnderwritingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Underwriting
        fields = '__all__'

class UnusedPrecedenceProcessSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    
    class Meta:
        model = UnusedPrecedenceProcess
        fields = '__all__'
