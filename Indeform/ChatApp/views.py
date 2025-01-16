from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Channel, Message, Membership
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChannelForm
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ChannelSerializer, MessageSerializer, MembershipSerializer
import logging

# Create your views here.
def home(request):
    return render(request, 'home.html')

#def room(request, room_name):
#    return render(request, 'chatroom.html', {
#        'room_name': room_name
#    })

"""
@login_required
def room(request, room_name):
    try:
        # Fetch the channel
        channel = Channel.objects.get(name=room_name)
    except Channel.DoesNotExist:
        return render(request, "403.html", {"room_name": room_name})

    # Check if the user is a member of the channel
    if not Membership.objects.filter(user=request.user, channel=channel).exists():
        return HttpResponseForbidden("You're not a member of this channel.")

    # Get the list of users in this channel
    users = Membership.objects.filter(channel=channel).values_list('user__username', flat=True)

    # Render the chatroom with the users in the channel
    return render(request, "chatroom.html", {
        "room_name": channel.id,
        #"room_name": room_name,
        "room": channel,
        "users": users,  # Pass the list of users
    })
"""
@login_required
def room(request, room_id):
    try:
        # Fetch the channel
        channel = Channel.objects.get(id=room_id)
    except Channel.DoesNotExist:
        return render(request, "403.html", {"room_id": room_id})

    # Check if the user is a member of the channel
    if not Membership.objects.filter(user=request.user, channel=channel).exists():
        return HttpResponseForbidden("You're not a member of this channel.")

    # Get the list of users in this channel
    users = Membership.objects.filter(channel=channel).values_list('user__username', flat=True)

    # Render the chatroom with the users in the channel
    return render(request, "chatroom.html", {
        "room_id": room_id,
        "room": channel,
        "users": users,
    })

'''
def add_user_to_channel(request, room_name):
    try:
        channel = Channel.objects.get(name=room_name)
    except Channel.DoesNotExist:
        messages.error(request, "Channel does not exist.")
        return redirect('chat:room', room_name=room_name)

    # Check if the current user is the creator of the room
    if channel.creator != request.user:
        return HttpResponseForbidden("Only the room creator can add users.")

    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' not found.")
            return redirect('chat:room', room_name=room_name)

        # Check if the user is already a member
        if Membership.objects.filter(user=user, channel=channel).exists():
            messages.warning(request, f"User '{username}' is already a member.")
        else:
            try:
                # Add the user to the channel
                Membership.objects.create(user=user, channel=channel)
                messages.success(request, f"User '{username}' has been added to the channel.")
            except IntegrityError:
                messages.error(request, f"Error adding user to the channel. Please try again. {user} {channel}")
                return redirect('chat:room', room_name=room_name)

    return redirect('chat:room', room_name=room_name)
'''
def add_user_to_channel(request, room_id):
    try:
        channel = Channel.objects.get(id=room_id)
    except Channel.DoesNotExist:
        messages.error(request, "Channel does not exist.")
        return redirect('chat:room', room_id=room_id)

    # Check if the current user is the creator of the room
    if channel.creator != request.user:
        return HttpResponseForbidden("Only the room creator can add users.")

    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' not found.")
            return redirect('chat:room', room_id=room_id)

        # Check if the user is already a member
        if Membership.objects.filter(user=user, channel=channel).exists():
            messages.warning(request, f"User '{username}' is already a member.")
        else:
            try:
                Membership.objects.create(user=user, channel=channel)
                messages.success(request, f"User '{username}' has been added to the channel.")
            except IntegrityError:
                messages.error(request, f"Error adding user to the channel. Please try again.")
                return redirect('chat:room', room_id=room_id)

    return redirect('chat:room', room_id=room_id)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('chat:home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('chat:home')
    else:
        return HttpResponse("You can't logout without POST request")
    
@login_required
def create_channel(request):
    if request.method == "POST":
        form = ChannelForm(request.POST)
        if form.is_valid():
            # Check if a channel with the same name already exists
            room_name = form.cleaned_data['name']
            if Channel.objects.filter(name=room_name).exists():
                form.add_error('name', 'A channel with this name already exists.')
            else:
                # Create the channel and set the creator
                channel = form.save(commit=False)
                channel.creator = request.user
                channel.save()

                # Add the creator to the Membership table
                Membership.objects.create(user=request.user, channel=channel)

                return redirect('chat:home')  # Redirect to home or any desired page
    else:
        form = ChannelForm()

    return render(request, 'chat/create_channel.html', {'form': form})


@login_required
def my_rooms(request):
    # Retrieve all rooms the current user is a member of
    memberships = Membership.objects.filter(user=request.user)
    rooms = [membership.channel for membership in memberships]
    return render(request, 'chat/my_rooms.html', {'rooms': rooms})

# UserRoomsAPIView
class UserRoomsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        memberships = Membership.objects.filter(user=request.user)
        rooms = [membership.channel for membership in memberships]
        serializer = ChannelSerializer(rooms, many=True)
        return Response(serializer.data)

# RoomMessagesAPIView
'''
class RoomMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, room_id):
        messages = Message.objects.filter(channel__id=room_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
'''

class RoomMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, room_id):
        messages = Message.objects.filter(channel__id=room_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


# CreateRoomAPIView
logger = logging.getLogger(__name__)
class CreateRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Copy the request data and set the creator to the current user
        data = request.data.copy()
        logger.debug(f"Request data: {data}")

        # Set the creator as the current user
        data['creator'] = request.user  # Directly add creator field as the current user

        # Serialize the data
        serializer = ChannelSerializer(data=data)
        if serializer.is_valid():
            # Save the channel and get the instance
            channel = serializer.save()  
            # Automatically add the creator as a member
            Membership.objects.create(user=request.user, channel=channel)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

# AddUserToRoomAPIView
class AddUserToRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, room_id):
        try:
            user = User.objects.get(username=request.data.get('username'))
            channel = Channel.objects.get(id=room_id)
            Membership.objects.create(user=user, channel=channel)
            return Response({"message": "User added to room."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Channel.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

# RegisterAPIView
class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists."}, status=400)
        User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."})

# SendMessageAPIView
class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            content = request.data.get('content')
            if not content:
                return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)

            channel = Channel.objects.get(id=room_id)
            message = Message.objects.create(
                channel=channel,
                sender=request.user,
                content=content
            )
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Channel.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)


class RoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request to list the rooms the user is part of."""
        memberships = Membership.objects.filter(user=request.user)
        rooms = [membership.channel for membership in memberships]
        serializer = ChannelSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Handle POST request to create a new room."""
        data = request.data.copy()
        logger.debug(f"Request data: {data}")

        # Set the creator to the current user
        data['creator'] = request.user.id  # Directly use the user ID for creator, it will be handled by the model as FK

        # Serialize the data
        serializer = ChannelSerializer(data=data)
        if serializer.is_valid():
            # Save the channel and get the instance
            channel = serializer.save()
            # Automatically add the creator as a member
            Membership.objects.create(user=request.user, channel=channel)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChannelMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        try:
            # Get the channel by the given ID
            channel = Channel.objects.get(id=channel_id)

            # Get all the memberships for this channel
            memberships = Membership.objects.filter(channel=channel)

            # Serialize the membership data
            serializer = MembershipSerializer(memberships, many=True)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response({'error': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)