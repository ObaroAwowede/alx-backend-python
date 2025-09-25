from rest_framework import serializers
from .models import User, Message, Conversation
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields =['id','first_name','last_name','email','password',
                 'phone_number','role','created_at','username']
        read_only_fields = ['id','created_at']
    
    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("A user with this email exists")
        return value
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    message_body = serializers.CharField(required=True)
    class Meta:
        model = Message
        fields = ['message_id','sender_id','conversation',
                  'message_body', 'sent_at','sender']
        read_only_fields = ['sender_id','message_id','sent_at']
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = User.objects.all(),
        write_only = True
    )
    participants_detail = UserSerializer(source='participants', many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id','participants','messages', 'created_at','participants_detail']
        read_only_fields = ['conversation_id', 'created_at']
        
    def get_messages(self, obj):
        messages = obj.messages.order_by('-sent_at')
        return MessageSerializer(messages, many=True, context=self.context).data

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value
    
    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation