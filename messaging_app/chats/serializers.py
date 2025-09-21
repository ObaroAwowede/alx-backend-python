from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['user_id','first_name','last_name','email',
                 'phone_number','role','created_at']
        read_only_fields = ['user_id','created_at']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    class Meta:
        model = Message
        fields = ['message_id','sender_id','conversation',
                  'message_body', 'sent_at']
        read_only_fields = ['sender_id','message_id','sent_at']
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only = True)
    messages = MessageSerializer(read_only = True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id','participants','messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']