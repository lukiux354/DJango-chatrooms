from django.urls import path
from . import views
from .views import (
    UserRoomsAPIView, RoomMessagesAPIView, CreateRoomAPIView,
    AddUserToRoomAPIView, RegisterAPIView, SendMessageAPIView, RoomAPIView, ChannelMembersAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'chat'


urlpatterns = [
    path('api/rooms/', RoomAPIView.as_view(), name='rooms'),
    path('api/messages/<int:room_id>/', RoomMessagesAPIView.as_view(), name='room_messages'),
    path('api/rooms/<int:room_id>/add-user/', AddUserToRoomAPIView.as_view(), name='add_user_to_room'),
    path('api/rooms/<int:channel_id>/members/', ChannelMembersAPIView.as_view(), name='channel_members'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/messages/<int:room_id>/', RoomMessagesAPIView.as_view(), name='room_messages'),
    path('api/messages/<int:room_id>/send/', SendMessageAPIView.as_view(), name='send_message'),
]