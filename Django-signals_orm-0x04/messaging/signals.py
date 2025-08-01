from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, Conversation
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
        
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip for new messages

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content has changed, log it
    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
            edited_by=instance.sender,  # or the editor if tracked differently
        )
        instance.edited = True  # Mark the message as edited
        
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    After a user is deleted, ensure:
    - Messages where they were sender or receiver are deleted.
    - MessageHistory entries they edited are deleted.
    - Notifications for that user are deleted.
    - Remove them from conversations; drop conversations with no participants.
    """
    try:
        # Explicitly delete messages where they were sender or receiver (cascade would have done sender/receiver side)
        Message.objects.filter(sender=instance).delete()
        Message.objects.filter(receiver=instance).delete()

        # Histories where they were the editor
        MessageHistory.objects.filter(edited_by=instance).delete()

        # Notifications for the user (cascade would normally handle it, but be explicit)
        Notification.objects.filter(user=instance).delete()

        # Clean up conversations: remove user from participant lists
        for convo in Conversation.objects.filter(participants_id=instance):
            convo.participants_id.remove(instance)
            # If conversation now has no participants, delete it
            if convo.participants_id.count() == 0:
                convo.delete()
                
    except Exception as e:
        # Log the error
        logger.error(f"Error cleaning up user data for user {instance.user_id}: {e}")