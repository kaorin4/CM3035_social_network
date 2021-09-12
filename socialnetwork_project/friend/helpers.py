from friend.models import FriendRequest

def find_friend_request(user_sender, user_receiver):
    try:
        return FriendRequest.objects.get(sender=user_sender, receiver=user_receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False