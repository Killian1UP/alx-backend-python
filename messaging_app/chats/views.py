from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Message, Conversation, User
from .serializers import MessageSerializer, ConversationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation


# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['participants_id']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants_id=self.request.user)
    
    def perform_create(self, serializer):
        # Save the conversation and add the authenticated user as a participant
        conversation = serializer.save()
        conversation.participants_id.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipantOfConversation]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender_id', 'conversation']
    ordering_fields = ['sent_at']
    
    def get_queryset(self):
        # Only return messages in conversations the user is part of
        return Message.objects.filter(conversation__participants_id=self.request.user)
    
    def perform_create(self, serializer):
        # Save message with authenticated user as sender
        serializer.save(sender_id=self.request.user.user_id)
