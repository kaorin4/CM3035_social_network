from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from chat.models import Chat, ChatMessage
from django.utils import timezone

# Create your views here.

class ChatView(View):
    template_name = 'chat/chat.html'

    def get_object(self):
        other_username  = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Chat.objects.get_or_create_chat(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get(self, request, **kwargs):

        context = {}
        context['user'] = self.request.user
        context['chat'] = self.get_object()
        context['friend'] = self.other_user
        context['messages'] = self.get_object().chatmessage_set.all()

        return render(request, self.template_name, context=context)


class ChatList(View):
    template_name = 'chat/chat_list.html'

    def get(self, request, **kwargs):

        context = {}
        chat_list = Chat.objects.by_user(self.request.user)
        chat_user_list = []

        for chat in chat_list:
            if chat.user1 != self.request.user:
                chat_user_list.append(chat.user1)
            elif chat.user2 != self.request.user:
                chat_user_list.append(chat.user2)

        context['chat_list'] = zip(chat_list, chat_user_list)

        has_chats = True if len(chat_list) > 0 else False

        context['has_chats'] = has_chats

        return render(request, self.template_name, context)
