from rest_framework import serializers
from .models import Channel, Message, Membership

class ChannelSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')  # Optional field for response

    class Meta:
        model = Channel
        fields = ['id', 'name', 'creator', 'creator_username', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')  # Include sender's username

    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender_username']

class MembershipSerializer(serializers.ModelSerializer):
    # This will return the username of the user
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Membership
        fields = ['user_username']  # Only show the username of the user in the response