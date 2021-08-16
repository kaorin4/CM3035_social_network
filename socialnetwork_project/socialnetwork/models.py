from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=False, blank=False)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', null=True, default='uploads/profile_pictures/default.png')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __unicode__(self):
        return self.user.username

    def get_friends(self):
        return ",".join([friend.username for friend in self.friends.all()])

    def add_to_friendlist(self, user):
        """
        Add user to friendlist
        """
        if not user in self.friends.all():
            self.friends.add(user)
            self.save()

    def remove_from_friendlist(self, user):
        """
        Delete user from friendlist
        """
        if user in self.friends.all():
            self.friends.remove(user)
            self.save()

    def is_friend(self, friend):
        """
        Check if its in your friend list
        """ 
        if friend in self.friends.all():
            return True
        return False


class Post(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)