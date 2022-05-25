from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from django.views.generic.base import View

from socialnetwork.models import UserProfile
from friend.models import *
# Create your views here.

@login_required
def send_friend_request(request, *args, **kwargs):
    """
    Creates a new friend request with the logged user as sender and provided user as received
    """

    user = request.user
    data = {}

    if request.method == "POST" and user.is_authenticated:
        receiver_username = request.POST.get("receiver_username")

        if receiver_username:
            receiver = User.objects.get(username=receiver_username)
            # get user friends list
            user_friends = user.userprofile.friends.all()

            is_friend = user_friends.filter(username=receiver.username)
            # not friend
            if not is_friend:

                # get friend requests
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)

                # user has sent friend requests
                if friend_requests:
                    for friend_request in friend_requests:
                        if friend_request.is_active:
                            raise Exception('Friend request sent')
                        else:
                            try:
                                # activate friend request
                                friend_request.activate_request()
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

    return JsonResponse(data)

@login_required
def accept_friend_request(request, *args, **kwargs):
    """
    Both users are added to each other's friendlist. Request is then set as not active
    """

    user = request.user
    data = {}

    if request.method == "POST" and user.is_authenticated:
        request_id = request.POST.get("request_id")

        if request_id:
            # get the request
            friend_request = FriendRequest.objects.get(id=request_id)
            # accept if logged user is the receiver of the request
            if friend_request.receiver == user:

                friend_request.accept_request()
                data["response"] = "Friend request accepted"
            # if logged user is not the receiver then its the wrong request
            else:
                data["response"] = "Error. not your request"

        else:
            data['response'] = "No request"
    else:
        data['response'] = "User not authenticated"

    return JsonResponse(data)

@login_required
def decline_friend_request(request, *args, **kwargs):
    """
    Friend request object is set to inactive
    """

    user = request.user
    data = {}

    if request.method == "POST" and user.is_authenticated:
        request_id = request.POST.get("request_id")

        if request_id:
            # get the request
            friend_request = FriendRequest.objects.get(id=request_id)
            # decline if logged user is the receiver of the request
            if friend_request.receiver == user:

                friend_request.deactivate_request()
                data["response"] = "Friend request declined"

            else:
                data["response"] = "Error. not your request"

        else:
            data['response'] = "No request"
    else:
        data['response'] = "User not authenticated"

    return JsonResponse(data)

@login_required
def cancel_friend_request(request, *args, **kwargs):
    """
    Friend request object is set to inactive
    """

    user = request.user
    data = {}

    if request.method == "POST" and user.is_authenticated:
        request_id = request.POST.get("request_id")

        if request_id:
            # get the request
            friend_request = FriendRequest.objects.get(id=request_id)
            # inactivate request if logged user sent it and the request is still active
            if friend_request.sender == user and friend_request.is_active:

                friend_request.deactivate_request()
                data["response"] = "Friend request cancelled"

            else:
                data["response"] = "Error. not your request"

        else:
            data['response'] = "No request"
    else:
        data['response'] = "User not authenticated"

    return JsonResponse(data)

@login_required
def friend_request_list(request, *args, **kwargs):
    """
    Returns list of friend requests sent and received of the logged user
    """

    user = request.user
    context = {}

    if user.is_authenticated:

        # get friend requests received
        friend_requests_received = FriendRequest.objects.filter(receiver=user, is_active=True)
        context['friend_requests_received'] = friend_requests_received

        # get friend requests sent
        friend_requests_sent = FriendRequest.objects.filter(sender=user, is_active=True)
        context['friend_requests_sent'] = friend_requests_sent

        return render(request, "friend/friend_request_list.html", context)

    else:
        messages.error(request, 'User no authenticated') 

@login_required
def friend_list(request, username, *args, **kwargs):
    """
    Returns list of friends of given username
    """

    user = request.user

    if user.is_authenticated:

        user_profile = User.objects.get(username=username)

        if user_profile:

            # get friends
            friends = user_profile.userprofile.friends.all()
            is_logged_user_profile = True if user.username == username else False

            context = {
                'friends': friends,
                'is_logged_user_profile': is_logged_user_profile
            }

            return render(request, "friend/friend_list.html", context)
        else:
            messages.error(request, 'User does not exist') 

    else:
        messages.error(request, 'User no authenticated') 









