from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import json

from socialnetwork.models import UserProfile
from friend.models import *
# Create your views here.

@login_required
def send_friend_request(request, *args, **kwargs):
    user = request.user
    data = {}

    if request.method == "POST" and user.is_authenticated:
        receiver_username = request.POST.get("receiver_username")

        if receiver_username:
            receiver = User.objects.get(username=receiver_username)

            # get friend requests
            friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)

            # user has sent friend requests
            if friend_requests:
                for friend_request in friend_requests:
                    if friend_request.is_active:
                        raise Exception('Friend request sent')
                    else:
                        try:
                            # create new friend request
                            friend_request = FriendRequest(sender=user, receiver=receiver)
                            friend_request.save()
                            data['response'] = "Friend request sent successfully"
                        except Exception as e:
                            data['response'] = str(e)
            else:
                # no friend requests
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                data['response'] = "Friend request sent successfully"
        else:
            data['response'] = "No receiver username provided"
    else:
        data['response'] = "User not authenticated"

    return HttpResponse(json.dumps(data), content_type="application/json")