from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from .models import Message, Conversation, Notification, MessageHistory

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'created_at', 'password', 'full_name'
        ]
        read_only_fields = ['user_id', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hashes the password properly
        user.save()
        return user

class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = UserSerializer(read_only=True)

    class Meta:
        model = MessageHistory
        fields = [
            'history_id',
            'old_content',
            'edited_at',
            'edited_by',
        ]
        read_only_fields = ['history_id', 'edited_at']
   
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    receiver_id = serializers.UUIDField(write_only=True)
    conversation = serializers.UUIDField(write_only=True)
    histories = MessageHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 'content', 'timestamp',
            'edited', 'histories'
        ]
        read_only_fields = ['message_id', 'timestamp', 'edited']
        
    def create(self, validated_data):
        sender = User.objects.get(user_id=validated_data.pop('sender_id'))
        receiver = User.objects.get(user_id=validated_data.pop('receiver_id'))
        conversation = Conversation.objects.get(conversation_id=validated_data.pop('conversation'))

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            conversation=conversation,
            **validated_data
        )
        return message
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(source='participants_id', many=True, read_only=True)
    participants_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participants_id', 'created_at', 'messages'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants_id')
        conversation = Conversation.objects.create()
        conversation.participants_id.set(participants)
        return conversation

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    message = MessageSerializer(read_only=True)
    message_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Notification
        fields = [
            'notification_id', 'user', 'user_id', 'message', 'message_id', 
            'is_read', 'created_at'
        ]
        read_only_fields = ['notification_id', 'created_at']

    def create(self, validated_data):
        user = User.objects.get(user_id=validated_data.pop('user_id'))
        message = Message.objects.get(message_id=validated_data.pop('message_id'))

        return Notification.objects.create(
            user=user,
            message=message,
            **validated_data
        )
        
