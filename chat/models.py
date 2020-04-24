from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()




    

def hex_uuid():
    return uuid.uuid4().hex

class Chat(models.Model):
    chat_uuid = models.CharField(default=hex_uuid, editable=False, max_length=32)
    participants = models.ManyToManyField(
    	User, related_name='participants', blank=True,
    )

    def __str__(self):
        return "{}".format(self.chat_uuid)


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='messages', 
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name="chat_message", null=True, blank=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.author.username