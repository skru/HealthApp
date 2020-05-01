from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import json

class ChatConsumer(WebsocketConsumer):

    def get_messages(self, data):
        # get message history and send back to broadcaster
        chat = Chat.objects.get(chat_uuid=data['chat_id'])
        messages = []
        for message in chat.chat_message.all():
            messages.append({
                "author": message.author.username,
                "author_name": message.author.get_full_name(),
                "message": message.content,
                "timestamp": str(message.timestamp.strftime('%d-%m-%Y %H:%M')),
        })
        content = {
            'type': 'get_messages',
            'message': messages,
        }
        return self.send_message(content)

    def add_message(self, data):
        # add new message to db, broadcast to websocket
        chat = Chat.objects.get(chat_uuid=data['chat_id'])
        user = User.objects.get(username=data['author'])
        message = Message.objects.create(
            author=user,
            content=data['message'],
            chat=chat
        )
        content = {
            'type': 'add_message',
            'message': message.content,
            'author': message.author.username,
            "author_name": message.author.get_full_name(),
            "timestamp": str(message.timestamp.strftime('%Y-%m-%d %H:%M')),
        }
        return self.send_chat_message(content)

    def init_peer(self, data):
        # send peer offer to websocket
    #/print("initing peer", data)
        content = {
            'type': 'init_peer',
            'message': data['message'],
            'author': data['author'],
        }
        return self.send_chat_message(content)

    def answer_peer(self, data):
        # send peer offer to websocket
        #print("answer peer", data)
        content = {
            'type': 'answer_peer',
            'message': data['message'],
            'author': data['author'],
        }
        return self.send_chat_message(content)

    def close_peer(self, data):
        # send peer offer to websocket
        #print("answer peer", data)
        content = {
            'type': 'close_peer',
            #'message': data['message'],
            'author': data['author'],
        }
        return self.send_chat_message(content)

    commands = {
        'get_messages': get_messages,
        'add_message': add_message,
        'init_peer': init_peer,
        'answer_peer': answer_peer,
        'close_peer': close_peer,
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
        self.commands[data['type']](self, data)

    def send_chat_message(self, content):
        # # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))

    # Send message history to broadcaster 
    def send_message(self, message):
        self.send(text_data=json.dumps({'message':message}))    