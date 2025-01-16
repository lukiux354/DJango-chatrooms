import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Channel
from django.contrib.auth.models import User

'''
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        #self.channel = await sync_to_async(Channel.objects.get)(id=self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch the last 50 messages asynchronously
        messages = await sync_to_async(
            lambda: list(
                Message.objects.filter(channel__name=self.room_name).order_by('-timestamp')[:50]
            )
        )()

        # Send the messages to the client in reverse order (oldest first)
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': [
                {
                    'message': message.content,
                    'username': await sync_to_async(lambda: message.sender.username)(),
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for message in reversed(messages)
            ]
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        username = data['username']

        # Fetch user and channel objects
        user = await sync_to_async(User.objects.get)(username=username)
        channel = await sync_to_async(Channel.objects.get)(name=self.room_name)

        # Save the message to the database and retrieve the timestamp
        message = await sync_to_async(Message.objects.create)(
            channel=channel,
            sender=user,
            content=message_content
        )

        # Send the message to the WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send the new message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))
'''


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Fetch the channel object by ID
        self.channel = await sync_to_async(Channel.objects.get)(id=self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Fetch last 50 messages asynchronously
        messages = await sync_to_async(
            lambda: list(
                Message.objects.filter(channel__id=self.room_id).order_by('-timestamp')[:50]
            )
        )()

        # Send messages to the client in reverse order
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': [
                {
                    'message': message.content,
                    'username': await sync_to_async(lambda: message.sender.username)(),
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for message in reversed(messages)
            ]
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        username = data['username']

        user = await sync_to_async(User.objects.get)(username=username)

        # Save the message
        message = await sync_to_async(Message.objects.create)(
            channel=self.channel,
            sender=user,
            content=message_content
        )

        # Broadcast the message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send the new message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))
