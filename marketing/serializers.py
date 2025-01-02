from rest_framework import serializers
from .models import InvitationCode, Invitation
from user.serializers import UserSerializer

class InvitationCodeSerializer(serializers.ModelSerializer):
    introducer_user_detail = UserSerializer(source='introducer_user', read_only=True)
    class Meta:
        model = InvitationCode
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    invitation_code_detail = InvitationCodeSerializer(source='invitation_code', read_only=True)
    invited_user_detail = UserSerializer(source='invited_user', read_only=True)
    class Meta:
        model = Invitation
        fields = '__all__'

