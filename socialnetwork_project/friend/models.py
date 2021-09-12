from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from socialnetwork.models import UserProfile

# Create your models here.
class FriendRequest(models.Model):
    """
    Friend request involves user sending it and the one receiving it
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    datetime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(blank=True, null=False, default=True)

    def accept_request(self):
        """
        Add both users to each other's friends list
        """
        sender = self.sender
        receiver = self.receiver
        
        # add friend to friends list
        if sender and receiver:
            sender.userprofile.friends.add(receiver)
            receiver.userprofile.friends.add(sender)
            self.is_active = False
            self.save()

    def deactivate_request(self):
        """
        Cancel or decline friend request 
        """
        self.is_active = False
        self.save()

    def activate_request(self):
        """
        Activate friend request. Shows up again
        """
        self.is_active = True
        self.save()


