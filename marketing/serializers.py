from rest_framework import serializers
from .models import Notification, InvitationCode, Invitation

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'tag', 'read', 'created_at']
        read_only_fields = ['title', 'message', 'tag', 'created_at']

class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

