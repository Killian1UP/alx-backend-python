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
    receiver_id = serializers.UUIDField(write_only=True)
    conversation_id = serializers.UUIDField(write_only=True)
    parent_message_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    histories = MessageHistorySerializer(many=True, read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'receiver_id', 'conversation_id', 'parent_message_id',
            'content', 'timestamp', 'edited', 'histories', 'replies', 'read'
        ]
        read_only_fields = ['message_id', 'timestamp', 'edited', 'replies']

    def validate(self, attrs):
        # optional: ensure business rules like sender/receiver in same conversation
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        # Validate conversation exists
        conversation_id = attrs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")

        # Ensure sender (request.user) is participant
        if request.user not in conversation.participants_id.all():
            raise serializers.ValidationError("Sender must be participant in the conversation.")

        # Optionally: ensure receiver is also a participant
        receiver_id = attrs.get('receiver_id')
        try:
            receiver = User.objects.get(user_id=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver does not exist.")
        if receiver not in conversation.participants_id.all():
            raise serializers.ValidationError("Receiver must be participant in the conversation.")

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')
        sender = request.user

        receiver_id = validated_data.pop('receiver_id')
        conversation_id = validated_data.pop('conversation_id')
        parent_message_id = validated_data.pop('parent_message_id', None)

        try:
            receiver = User.objects.get(user_id=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver does not exist.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")

        parent_message = None
        if parent_message_id:
            try:
                parent_message = Message.objects.get(message_id=parent_message_id)
            except Message.DoesNotExist:
                raise serializers.ValidationError("Parent message does not exist.")

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            conversation=conversation,
            parent_message=parent_message,
            **validated_data
        )
        return message

    def get_replies(self, obj):
        replies_qs = obj.replies.all().select_related('sender', 'receiver')
        return MessageSerializer(replies_qs, many=True, context=self.context).data


        
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
