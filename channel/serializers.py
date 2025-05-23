from rest_framework import serializers
from .models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.ReadOnlyField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'description', 'owner', 'subscriber_count', 'created_at']
        read_only_fields = ['owner', 'subscriber_count', 'created_at']
