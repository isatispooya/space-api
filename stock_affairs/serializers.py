from rest_framework import serializers
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence , Underwriting , UnusedPrecedenceProcess , Appendices , ProcessDescription
from companies.serializers import CompanySerializer
from user.serializers import UserSerializer
from transactions.serializers import PaymentSerializer
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

class UnusedPrecedenceProcessSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    
    class Meta:
        model = UnusedPrecedenceProcess
        fields = '__all__'


class AppendicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appendices
        fields = '__all__'

class ProcessDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDescription
        fields = '__all__'

class UnderwritingSerializer(serializers.ModelSerializer):
    appendices = AppendicesSerializer(read_only=True)
    process_detail = UnusedPrecedenceProcessSerializer(source='unused_precedence_process', read_only=True)
    payment_detail = PaymentSerializer(source='payment', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    process_description = ProcessDescriptionSerializer(read_only=True)

    class Meta:
        model = Underwriting
        fields = '__all__'

