from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name="notification"
    )
    recipients = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    
    def __str__(self):
        return super().__str__()