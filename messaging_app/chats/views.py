from django.shortcuts import render
from rest_framework import serializers, viewset, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message

class ConversationViewSet(viewset.ModelViewSet):
    queryset= Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # This ensures the authenticated user is included in participants
        participant_ids = request.data.get('participants', [])
        if str(request.user.user_id) not in [str(id) for id in participant_ids]:
            participant_ids.append(str(request.user.user_id))
        # This is to Validate participants
        if len(participant_ids) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()

        serializer = self.get_serializer(conversation)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only messages in conversations where the authenticated user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # This sets the sender as the authenticated user
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("This conversation does not exist.")

        # This ensures the user is a participant in the conversation
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            raise serializers.ValidationError("You are not a participant in this conversation.")
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=serializer.validated_data['message_body']
        )
        serializer = self.get_serializer(message)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def conversation_messages(self, request, pk=None):
        # This is used to list all messages in a specific conversation
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("This conversation does not exist.")
        # This ensures the user is a participant
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            raise serializers.ValidationError("You are not a participant in this conversation.")
        messages = Message.objects.filter(conversation=conversation).order_by('-sent_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)