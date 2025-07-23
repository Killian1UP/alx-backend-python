from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # First check if the user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation related to the message
        user = request.user
        
        # Handle Message instance (assumes obj is a Message with obj.conversation)
        conversation = getattr(obj, 'conversation', None)
        
        if conversation is None:
            return False
        
        return user in conversation.participants_id.all()