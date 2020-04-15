from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import json

class ChatConsumer(WebsocketConsumer):
    def add_message(self, data):
        user_contact = User.objects.get(username=data['author'])
        message = Message.objects.create(
            author=user_contact,
            content=data['message'])
        current_chat = Chat.objects.get(id=data['chat_id'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'add_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        #'fetch_messages': fetch_messages,
        'add_message': add_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

        # message = text_data_json['message']
        # command = text_data_json['command']
        # author = text_data_json['author']
        # print("msg: ", message, "cmd: ", command, "AUT: ", author)
    def send_chat_message(self, content):
        # # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                # 'command': command,
                # 'author': author
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # command = event['command']
        # author = event['author']
        # print(message, command, author)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            # 'command': command,
            # 'author': author
        }))