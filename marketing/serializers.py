from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'tag', 'read', 'created_at']
        read_only_fields = ['title', 'message', 'tag', 'created_at']
