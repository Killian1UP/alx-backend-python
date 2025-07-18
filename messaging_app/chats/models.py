import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserRole(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'
    
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    password_hash = models.CharField(max_length=128, editable=False)
    
    def save(self, *args, **kwargs):
        # Sync password_hash with the hashed password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        self.password_hash = self.password
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants_id = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    