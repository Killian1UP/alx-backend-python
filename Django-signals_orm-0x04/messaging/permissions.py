from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # Require authentication globally
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Derive the conversation depending on object type
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        # Only participants may access or mutate
        if request.method in permissions.SAFE_METHODS:
            return user in conversation.participants_id.all()

        # For writes (POST/PUT/PATCH/DELETE), also require participation
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return user in conversation.participants_id.all()

        return False
