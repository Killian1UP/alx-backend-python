from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from .models import Message
from .models import Conversation

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
        read_only_fields = ['user_id', 'created_id']
    
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
    
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    conversation = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']
        
    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        conversation_id = validated_data.pop('conversation')
        
        # Convert UUIDs to model instances
        sender = User.objects.get(user_id=sender_id)
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        
        message = Message.objects.create(
            sender_id=sender,
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
    