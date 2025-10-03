from django.db.models.signals import post_save
from models import Message, Notification
from django.dispatch import receiver

@receiver(post_save, sender= Message)
def create_notification(sender, instance, created, **kwargs):
    if hasattr(instance, 'notification'):
        return
    
    Notification.objects.create(
        user=instance,
        recipient=instance.receiver
    )