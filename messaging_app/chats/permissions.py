from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # First check if the user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation related to the message
        user = request.user
        conversation = getattr(obj, 'conversation', None)
        
        if conversation is None:
            return False
        
        # For safe methods (GET, HEAD, OPTIONS), allow if user is participant
        if request.method in permissions.SAFE_METHODS:
            return user in conversation.participants_id.all()

        # For unsafe methods (PUT, PATCH, DELETE), also require user is participant
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return user in conversation.participants_id.all()

        # Deny all other methods by default
        return False