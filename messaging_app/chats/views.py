from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['participants_id']
    ordering_fields = ['created_at']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender_id', 'conversation']
    ordering_fields = ['sent_at']