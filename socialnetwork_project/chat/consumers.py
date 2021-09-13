from channels.consumer import AsyncConsumer, StopConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from chat.models import Chat, ChatMessage
from asgiref.sync import sync_to_async
import json
import datetime

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        logged_user = self.scope['user']
        friend_username = self.scope['url_route']['kwargs']['username']
        friend_user = await sync_to_async(User.objects.get)(username=friend_username)
        # get or create chat object 
        self.chat_obj = await sync_to_async(Chat.objects.get_or_create_chat)(logged_user, friend_user)
        self.room_name = f'{self.chat_obj.room_name}'

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

        print(f'[{self.channel_name}] - You are connected')

    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')

        msg = json.dumps({
            'text': event.get('text'),
            'username': self.scope['user'].username
        })

        await self.save_message(event.get('text'))

        # send to room
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': msg
            }
        )

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        # remove channel from room name
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        raise StopConsumer()

    @database_sync_to_async
    def save_message(self, content):
        """
        Save chat message into the database
        """
        # store message in db
        ChatMessage.objects.create(
            chat = self.chat_obj,
            sender = self.scope['user'],
            content = content
        )
        
        chat = Chat.objects.get(id=self.chat_obj.id)
        chat.updated_at = datetime.datetime.now()
        chat.save()


