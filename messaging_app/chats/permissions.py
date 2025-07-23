from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # First check if the user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation related to the message
        return request.user in obj.conversation.participants_id.all()