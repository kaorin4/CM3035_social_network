from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class ChatManager(models.Manager):

    def get_or_create_chat(self, user1, user2):
        chat = self.get_queryset().filter((Q(user1=user1) and Q(user2=user2)) | (Q(user1=user2) and Q(user2=user1)))
        if chat.exists():
            return chat.first()
        else:
            chat = self.create(
                user1 = user1,
                user2 = user2,
            )
            return chat

    def by_user(self, user):
        "Return list of chats by user"
        return self.get_queryset().filter(Q(user1=user) | Q(user2=user))


class Chat(models.Model):

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    @property
    def room_name(self):
        "Returns chat room id"
        return f'{self.id}'
        
class ChatMessageManager(models.Manager):

	def order_messages(self, chat):
		ordered_messages = ChatMessage.objects.filter(chat=chat).order_by("-timestamp")
		return ordered_messages

class ChatMessage(models.Model):

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ChatMessageManager()

    def __str__(self) -> str:
        return self.content


