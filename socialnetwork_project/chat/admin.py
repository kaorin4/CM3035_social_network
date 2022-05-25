from django.contrib import admin
from chat.models import Chat, ChatMessage
# Register your models here.

class MessageInline(admin.StackedInline):
    model = ChatMessage
    fields = ('sender', 'content')
    readonly_fields = ('sender', 'content')


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    inlines = (MessageInline,)

admin.site.register(Chat, ChatAdmin)