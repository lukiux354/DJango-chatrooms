from django.urls import path
from . import views
from .views import (
    UserRoomsAPIView, RoomMessagesAPIView, CreateRoomAPIView,
    AddUserToRoomAPIView, RegisterAPIView, SendMessageAPIView, RoomAPIView, ChannelMembersAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'chat'

#urlpatterns = [
#    path("", views.my_rooms, name='home'),
#    path("register/", views.register_view, name='register'),
#    path("login/", views.login_view, name='login'),
#    path("logout/", views.logout_view, name='logout'),
#    path('create-channel/', views.create_channel, name='create_channel'),
#    path("my-rooms/", views.my_rooms, name="my_rooms"),
#    path('<str:room_name>/add-user/', views.add_user_to_channel, name='add_user_to_channel'),
#    path("<str:room_name>/", views.room, name='room'),
#]

urlpatterns = [
    path('api/rooms/', RoomAPIView.as_view(), name='rooms'),
    #path('api/rooms/', CreateRoomAPIView.as_view(), name='create_room'),
    #path('api/rooms/', UserRoomsAPIView.as_view(), name='user_rooms'),
    path('api/messages/<int:room_id>/', RoomMessagesAPIView.as_view(), name='room_messages'),
    path('api/rooms/<int:room_id>/add-user/', AddUserToRoomAPIView.as_view(), name='add_user_to_room'),
    path('api/rooms/<int:channel_id>/members/', ChannelMembersAPIView.as_view(), name='channel_members'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/messages/<int:room_id>/', RoomMessagesAPIView.as_view(), name='room_messages'),
    path('api/messages/<int:room_id>/send/', SendMessageAPIView.as_view(), name='send_message'),
]