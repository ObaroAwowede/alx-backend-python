from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['user_id','first_name','last_name','email',
                 'phone_number','role','created_at']
        read_only_fields = ['user_id','created_at']
    
    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("A user with this email exists")
        
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    message_body = serializers.CharField(required=True)
    class Meta:
        model = Message
        fields = ['message_id','sender_id','conversation',
                  'message_body', 'sent_at']
        read_only_fields = ['sender_id','message_id','sent_at']
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only = True)
    messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id','participants','messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
        
    def get_messages(self, obj):
        messages = obj.messages.order_by('-sent_at')
        return MessageSerializer(messages, many=True, context=self.context).data

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value