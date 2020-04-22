from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username


class Chat(models.Model):
    chat_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
    	User, related_name='participants', blank=True,
    )
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)