from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=215, null=False)
    last_name = models.CharField(max_length=215, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=215, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('guest','Guest'),
            ('host','Host'),
            ('admin','Admin')
        ],
        null= False
    )
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    participants_id = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]
        
    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at'])
        ]
