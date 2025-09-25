from django.urls import path, include 
from rest_framework import routers 
from rest_framework_nested import routers 
from .views import ConversationViewSet, MessageViewSet, UserListCreateView
from . import auth

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserListCreateView.as_view(), name = 'user-list-create-view'),
    path('token/', auth.get_token, name = 'token-obtain-view'),
    path('token/refresh/', auth.refresh_token, name = 'token-refresh-view'),
    path('', include(conversations_router.urls)),
]