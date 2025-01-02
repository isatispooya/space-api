from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Notification, InvitationCode, Invitation

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'tag', 'read', 'created_at']
        read_only_fields = ['title', 'message', 'tag', 'created_at']

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

