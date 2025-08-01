from django.shortcuts import render
from rest_framework import viewsets, filters, mixins, exceptions
from .models import Message, Conversation, User, Notification, MessageHistory
from .serializers import MessageSerializer, ConversationSerializer, UserSerializer, NotificationSerializer, MessageHistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .pagination import MessagePagination
from .filters import MessageFilter
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action


# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('created_at')
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
        return (Conversation.objects
            .filter(participants_id=self.request.user)
            .prefetch_related('participants_id', 'messages__sender', 'messages__receiver')
            .order_by('-created_at'))
    
    def perform_create(self, serializer):
        # Save the conversation and add the authenticated user as a participant
        conversation = serializer.save()
        conversation.participants_id.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender', 'receiver', 'conversation']
    ordering_fields = ['timestamp']
    filterset_class = MessageFilter
    
    def get_queryset(self):
        # Only return messages in conversations the user is part of
        return (
        Message.objects
        .filter(conversation__participants_id=self.request.user)
        .select_related('sender', 'receiver', 'conversation', 'parent_message')  # FK joins
        .prefetch_related('replies')  # reverse FK for nested replies
        .order_by('-timestamp')
    )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        # sender is always request.user
        serializer.save(sender=self.request.user)

        
    def _build_thread_tree(self, root_message):
        def serialize_node(msg):
            data = self.get_serializer(msg).data

            children = Message.objects.filter(parent_message=msg).select_related(
                'sender', 'receiver'
            ).order_by('timestamp')

            data['replies'] = [serialize_node(child) for child in children]
            return data

        return serialize_node(root_message)
        

    @action(detail=True, methods=["get"])
    def thread(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        message_id = self.kwargs.get('pk')

        # ensure message exists under that conversation
        try:
            message = (
                Message.objects
                .select_related('sender', 'receiver', 'parent_message', 'conversation')
                .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
                .get(message_id=message_id, conversation__conversation_id=conversation_id)
            )
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # permission: participant in conversation
        if request.user not in message.conversation.participants_id.all():
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        nested = self._build_thread_tree(message)
        return Response(nested)
        
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MessageHistory.objects.filter(edited_by=self.request.user).order_by('-edited_at')
    
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    # require password confirmation in body
    password = request.data.get('password')
    if not password or not user.check_password(password):
        return Response({"detail": "Incorrect or missing password."}, status=status.HTTP_403_FORBIDDEN)
    # perform delete
    user.delete()
    return Response({"detail": "Account deleted."}, status=status.HTTP_200_OK)
    