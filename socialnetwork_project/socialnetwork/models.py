from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.core.validators import MaxValueValidator

# Create your models here.

class UserProfile(models.Model):
    """
    Profile of a user, includes additional fields such as birthdate, picture
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=False, blank=False, validators=[MaxValueValidator(limit_value=date.today)])
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', null=True, default='uploads/profile_pictures/default.png')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def is_friend(self, friend):
        """
        Check if its in your friend list
        """ 
        if friend in self.friends.all():
            return True
        return False


class Post(models.Model):
    """
    Post includes author, text content, image and date it was created
    """

    text = models.TextField()
    image = models.ImageField(upload_to='uploads/posts_pictures', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)